def text_processing(text1, text2):
    text1 = text1.split(':')[0]
    text2 = text2.split(':')[0]
    to_do = 'skip'
    video_length = 100
    error_status = 0
    if len(text1) == 1:
        try:
            if int(text1[0]) <= 2:
                to_do = 'text1'
                video_length = int(text1[0])
                error_status = 0
        except:
            error_status = 1
            pass
    if len(text1) == 2:
        if text1[0] != '1' and text1[0] != '2' and text1[0] != '3' and text1[0] != '4' and text1[0] != '5' and text1[0] != '6' and text1[0] != '7' and text1[0] != '8' and text1[0] != '9':
            text1 = text1[1:len(text1)]
            try:
                if int(text1[0]) <= 2:
                    to_do = 'text1'
                    video_length = int(text1[0])
                    error_status = 0
            except:
                error_status = 1
                pass
    if len(text1) == 3:
        text1 = text1[1:len(text1)]
        if text1[0] != '1' and text1[0] != '2' and text1[0] !='3' and text1[0] != '4'and text1[0] !='5'and text1[0] !='6'and text1[0] !='7'and text1[0] != '8'and text1[0] != '9':
            text1 = text1[1:len(text1)]
            try:
                if int(text1[0]) <= 2:
                    to_do = 'text1'
                    video_length = int(text1[0])
                    error_status = 0
            except:
                error_status = 1
                pass

    if len(text2) == 1:
        try:
            if int(text2[0]) <= 2 and int(text2[0]) < video_length:
                to_do = 'text2'
                error_status = 0
        except:
            error_status = 1
            pass
    if len(text2) == 2:
        if text2[0] !='1'and text2[0] !='2'and text2[0] !='3'and text2[0] !='4'and text2[0] !='5'and text2[0] !='6'and text2[0] != '7'and text2[0] !='8'and text2[0] !='9':
            try:
                text2 = text2[1:len(text2)]
                if int(text2[0]) <= 2 and int(text2[0]) < video_length:
                    to_do = 'text2'
                    error_status = 0
            except:
                error_status = 1
                pass
    if len(text2) == 3:
        try:
            text2 = text2[1:len(text2)]
            if text2[0] !='1'and text2[0] !='2'and text2[0] !='3'and text2[0] !='4'and text2[0] !='5'and text2[0] !='6'and text2[0] !='7'and text2[0] != '8'and text2[0] !='9':
                text2 = text2[1:len(text2)]
                if int(text2[0]) <= 2 and int(text2[0]) < video_length:
                    to_do = 'text2'
                    error_status = 0
        except:
            error_status = 1
            pass
    
    return to_do, error_status
