from aiogram import Router
from aio.handlers.routers.router_for_start import router as router_start
from aio.handlers.callback_handlers.callback_for_industry import router as router_callback_industry
from aio.handlers.callback_handlers.callbackhandler import router as router_callback
from aio.handlers.callback_handlers.callback_change_register import router as router_for_changed
from aio.handlers.callback_handlers.callback_changeanketa import router as router_anketa
from aio.handlers.callback_handlers.skip_callback import router as router_skip
from aio.handlers.ref_handlers.ref_handler import router as router_ref
from aio.handlers.ref_handlers.callback_ref.callback_ref import router as router_callback_ref
from aio.handlers.ref_handlers.callback_ref.callback_pastet_code import router as router_pastet_ref
from aio.handlers.search_handlers import router as router_search
from aio.handlers.routers.router_lije import router as router_like
from admin_panel.for_admin_ad import router as admin_ad_router
from aio.handlers.language_handler import router as router_language
from aio.handlers.ref_handlers.callback_ref.keyboard_callback import router as router_keyboard_ref
from aio.handlers.callback_handlers.callback_settings import router as router_setting
from aio.handlers.callback_handlers.callback_profile import router as router_callback_profile
from aio.handlers.callback_handlers.callback_back.callback_main_menu import router as router_back_main
from aio.report_handler import router as router_report
from aio.handlers.callback_handlers.change_lang_ind.change_industry import router as router_indusry_land_change
from aiogram import Dispatcher
from aio.middleware.auto_activate import AutoActivateMiddleware


dp = Dispatcher()


router = Router(name="global_router")
router.include_router(router_report)
router.include_router(router_indusry_land_change)
router.include_router(router_start)
router.include_router(router_callback)
router.include_router(router_callback_industry)
router.include_router(router_for_changed)
router.include_router(router_anketa)
router.include_router(router_skip)
router.include_router(router_ref)
router.include_router(router_callback_ref)
router.include_router(router_pastet_ref)
router.include_router(router_search)
router.include_router(router_like)
router.include_router(admin_ad_router)
router.include_router(router_language)
router.include_router(router_keyboard_ref)
router.include_router(router_setting)
router.include_router(router_callback_profile)
router.include_router(router_back_main)

dp.include_router(router)
dp.message.middleware(AutoActivateMiddleware())
dp.callback_query.middleware(AutoActivateMiddleware())