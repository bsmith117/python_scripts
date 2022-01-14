def buoy_plot_grid(buoy_list,name_list,location):
    import datetime
    from surfline_extract_V3 import surfline_extract
    import cv2
    surfline_extract(name_list, buoy_list)
    buoy_img = '/Users/Brandon/PycharmProjects/WaveApp/bouy_plot_output/'
    #image_name = name + '_plot.png'
    #img_path = directory + image_name

    img1 = cv2.imread(buoy_img + name_list[0] + '_plot.png')
    img2 = cv2.imread(buoy_img + name_list[1] + '_plot.png')
    #img3 = cv2.imread(buoy_img + name_list[2] + '_plot.png')
    def concat_vh(list_2d):

        # return final image
        return cv2.vconcat([cv2.hconcat(list_h)
                            for list_h in list_2d])
    # image resizing

    img1_s = cv2.resize(img1, dsize=(0, 0), fx=1, fy=1)
    img2_s = cv2.resize(img2, dsize=(0, 0), fx=1, fy=1)
    #img3_s = cv2.resize(img3, dsize=(0, 0), fx=1, fy=1)
    # function calling
    img_tile_1 = concat_vh([[img2_s,img1_s]])
    cv2.imwrite('/Users/Brandon/PycharmProjects/WaveApp/report_grid/report_grid_' + location + '.jpg', img_tile_1)
