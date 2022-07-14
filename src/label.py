import numpy
import cv2
import imutils

def quick_lable():
    img = cv2.imread(filename)

def create_label(img,SLIC_width,SLIC_height,SLIC_centers,SLIC_clusters):
    label = 0
    adj_label = 0
    lims = int(SLIC_width * SLIC_height / SLIC_centers.shape[0])
    
    new_clusters = -1 * numpy.ones(img.shape[:2]).astype(numpy.int64)
    elements = []
    for i in range(SLIC_width):
        for j in range(SLIC_height):
            if new_clusters[j, i] == -1:
                elements = []
                elements.append((j, i))
                for dx, dy in [(-1,0), (0,-1), (1,0), (0,1)]:
                    x = elements[0][1] + dx
                    y = elements[0][0] + dy
                    if (x>=0 and x < SLIC_width and 
                        y>=0 and y < SLIC_height and 
                        new_clusters[y, x] >=0):
                        adj_label = new_clusters[y, x]
                    #end
                #end
            #end

            count = 1
            counter = 0
            while counter < count:
                for dx, dy in [(-1,0), (0,-1), (1,0), (0,1)]:
                    x = elements[counter][1] + dx
                    y = elements[counter][0] + dy

                    if (x>=0 and x<SLIC_width and y>=0 and y<SLIC_height):
                        if new_clusters[y, x] == -1 and SLIC_clusters[j, i] == SLIC_clusters[y, x]:
                            elements.append((y, x))
                            new_clusters[y, x] = label
                            count+=1
                        #end
                    #end
                #end

                counter+=1
            #end
            if (count <= lims >> 2):
                for counter in range(count):
                    new_clusters[elements[counter]] = adj_label
                #end

                label-=1
            #end

            label+=1
        #end
    #end

    SLIC_new_clusters = new_clusters
#end
