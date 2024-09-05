'''Font definitions'''
log_it('Fonts.py -loaded on '+str(datetime.datetime.now()),'a')
def add_font_to_registry(font_size):
    font_path = os.path.join('res','Fonts','DejaVuSansCondensed.ttf')
    with dpg.font_registry(tag='Font_registry'):
        '''Add a font registry.'''
        
        with dpg.font(font_path, font_size,tag='DejaVu') as font_18:
            dpg.add_font_range(0x0300, 0x03ff)
            dpg.add_font_range(0x0200, 0x02ff)
            dpg.add_font_range(0x2080, 0x209C)
            default_font = font_18
        dpg.bind_font(default_font)





add_font_to_registry(init_font_size)




