import random
import string
import logging
from contextlib import contextmanager
from datetime import datetime, timezone
from enum import Enum
from subprocess import CalledProcessError

from ereuse_utils import cmd

from ereuse_workbench.utils import Dumpeable, Severity
from ereuse_workbench.config import WorkbenchConfig


class EraseType(Enum):
    EraseBasic = 'EraseBasic'
    EraseSectors = 'EraseSectors'

    def __str__(self):
        return self.value


class Measurable(Dumpeable):
    @contextmanager
    def measure(self):
        self.start_time = datetime.now(timezone.utc)
        yield
        self.end_time = datetime.now(timezone.utc)
        assert self.end_time > self.start_time


class Erase(Measurable):
    """Erase data storage units (HDD / SSD) and saves a report."""

    def __init__(self, type: EraseType, steps: int, zeros: bool, callback) -> None:
        assert steps >= 1, 'Steps must be 1 or more.'
        self.type = type
        self._steps = steps
        self._zeros = zeros
        self.steps = []
        self.severity = Severity.Info
        self._callback = callback

    def run(self, dev: str):
        with self.measure():
            try:
                self._run(dev)
            except CannotErase:
                self.severity = Severity.Error
                raise
            except Exception as e:
                logging.error('%s %s finished with exception:', self.type, dev)
                logging.exception(e)
                raise

    def _run(self, dev: str):
        for step_info in WorkbenchConfig.load_steps():
            step = Step(
                StepType.StepZero
                if step_info.get('type') == '0' else
                StepType.StepRandom,
                self._callback,
            )
            if step_info.get('method') == 'EraseBasic':
                step.erase_basic(dev)
            elif step_info.get('method') == 'EraseSectors':
                step.erase_sectors(dev)
            else:
                print(f"Unknown step {step_info.get('method')}.")
            self.steps.append(step)

    @staticmethod
    def compute_total_steps(type: EraseType, erase_steps: int, erase_zeros: bool) -> int:
        """Gets the number of steps the erasure settings will cause."""
        if type == EraseType.EraseSectors:
            #  badblocks does an extra step to check
            steps += 1
        return len(WorkbenchConfig.load_steps())*2 or steps


class StepType(Enum):
    StepZero = 'StepZero'
    StepRandom = 'StepRandom'


class Step(Measurable):
    def __init__(self, type: StepType, callback) -> None:
        self.type = type
        self.severity = Severity.Info
        self._zeros = '-vn 1' if type == StepType.StepRandom else '-zvn 0'
        self._callback = callback

    @contextmanager
    def _manage_erasure(self, dev):
        with self.measure():
            try:
                yield
            except CalledProcessError as e:
                logging.error('%s %s finished with exception:', self.type, dev)
                logging.exception(e)
                self.severity = Severity.Error
                raise CannotErase(dev)
            except Exception as e:
                logging.error('%s %s finished with exception:', self.type, dev)
                logging.exception(e)
                raise
            else:
                logging.info('%s %s successfully finished', self.type, dev)

    def erase_basic(self, dev: str):
        logging.info('%s %s with Erase Basic', self.type, dev)
        with self._manage_erasure(dev):
            self._badblocks = False
            progress = cmd.ProgressiveCmd('shred', self._zeros, dev,
                                          number_chars={1, 2, 3},
                                          callback=self._callback)
            progress.run()

    def erase_sectors(self, dev: str):
        logging.info('%s %s with Erase Sectors', self.type, dev)
        with self._manage_erasure(dev):
            self._badblocks = True
            if self.type == StepType.StepRandom:
                # Create hexadecimal pattern.
                erasure_pattern = '0x' + ''.join(
                    random.choice(string.hexdigits) for _ in range(8))
            else:
                # Write zeros.
                erasure_pattern = "0"
            progress = cmd.ProgressiveCmd(
                'badblocks', '-st', erasure_pattern,
                '-w', dev,
                number_chars=cmd.ProgressiveCmd.DECIMALS,
                decimal_numbers=2,
                read=35,
                callback=self._call
            )
            progress.run()

    def _call(self, increment, percentage):
        # Performs a sanity check for badblocks
        # todo this uglily patches an error of ProgressiveCmd
        if self._badblocks:
            if increment > 0.1:
                return
        self._callback(increment, percentage)


class CannotErase(Exception):
    def __str__(self) -> str:
        return 'Cannot erase the data storage {}'.format(self.args[0])
