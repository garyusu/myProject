import cv2
import numpy as np

def coordParse(point,screen,video):
    x = int((point[0]-151)*video[0]/screen[0])+50          # video offset in html:  151,30
    y = int((point[1]-30)*video[1]/screen[1])+50
    return x, y

def accum(frm, center, r):
    h,w = frm.shape[:2]
    mask = np.zeros((h,w),np.uint8)
    cv2.circle(mask,center,r,15,-1)
    acc = cv2.add(frm,mask)
    return acc


def heatmapping(json_list, file, name):
    cap = cv2.VideoCapture(file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(1000/fps)
    print(f'FPS: {fps}')

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('./static/res/'+name+'.avi', fourcc, fps, (1380, 820))

    # debug
    fourcc2 = cv2.VideoWriter_fourcc(*'DIVX')
    out2 = cv2.VideoWriter('./static/res/debug.avi', fourcc2, fps, (1380, 820))
    # end

    i = 0  # init frame
    heat = np.zeros((820,1380),np.uint8)

    while cap.isOpened():
        ret, frame = cap.read()
        if (ret):
            padframe = cv2.copyMakeBorder(frame.copy(), 50, 50, 50, 50, cv2.BORDER_CONSTANT)
            
            r_cent = json_list[i]['x'], json_list[i]['y']      # video offset in html:  151,30
            x, y = coordParse(r_cent,(1600,900),(1280,720))
            print(f'frm size: {padframe.shape[0]}, {padframe.shape[1]}')
            print(x, y)
            
            if (x>=0) and (x<=1380) and (y>=0) and (y<=820):
                print('TRUE')
                heat = accum(heat, (x,y), 60)
            
            heatmap = cv2.applyColorMap(heat,cv2.COLORMAP_JET)      # binary to heatmap-like
            # debug
            out2.write(heatmap)
            #
            res = cv2.addWeighted(padframe, 0.5, heatmap, 0.5, 0)
            out.write(res)
            i+=1
        else:
            break
    
    cap.release()
    out.release()
    out2.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    pass