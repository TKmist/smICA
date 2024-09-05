
log_it('Handlers -loaded on '+str(datetime.datetime.now()),'a')
with dpg.handler_registry(tag='handlers_registry'):
    dpg.add_key_press_handler(tag ='keyword_handler_all',callback=callback_Keyword_key)

