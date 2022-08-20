from aiogram import Dispatcher
from controls.settings import ACTIVE_TELEINTRFACE_MODULES
import importlib
import logging
from types import FunctionType

logger = logging.getLogger(__name__)


async def dispatcher_register_handlers(dp: Dispatcher):
    for module_name in ACTIVE_TELEINTRFACE_MODULES:
        try:
            module = importlib.import_module('.handlers', module_name)
            await getattr(module, 'register_handlers')(dp)
        except ModuleNotFoundError as e:
            logger.warning(e)
        except TypeError as e:
            logger.warning(e)
            continue
