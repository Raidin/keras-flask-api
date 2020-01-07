import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

def SelectiveSearch(img):
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    ss.setBaseImage(img)
    ss.switchToSelectiveSearchFast()
    ssresults = ss.process()

    # ssresults의 bbow 좌표 포맷 x, y, w, h
    # 현재 코드에서 사용되는 bbox 좌표 포맷은 xmin, ymin, xmax, ymax
    # IOU 계산 및  DrawBox 함수 모듈화를 위해 convert
    ssresults[:, 2] = ssresults[:, 0] + ssresults[:, 2]
    ssresults[:, 3] = ssresults[:, 1] + ssresults[:, 3]
    return ssresults

def FeedForward(model, data, img, out_dim):
    results = np.array([], dtype=np.float32).reshape(0, out_dim)
    for i in data:
        timg = img[int(i[1]) : int(i[3]), int(i[0]) : int(i[2])]
        rimg = cv2.resize(timg, (224, 224), interpolation = cv2.INTER_AREA)
        rimg = np.divide(rimg, 255.)
        inimg = np.expand_dims(rimg, axis=0)
        output = model.predict(inimg)
        results = np.vstack([results, output])

    return results

def PredictObject(model, rois, img):
    # Classification Feed Forward
    results = FeedForward(model, rois, img, 2)

    idx = np.where(results[:,1] > 0.75)[0]
    rois = rois[idx]
    results = results[idx, 1]
    predict = np.column_stack([rois, results])

    return predict

def RefineBoundingBox(predict_bbox, reg_output):
    refine_bbox = predict_bbox.copy()

    if refine_bbox.shape[0] > 0:
        refine_bbox[:, 0] = np.trunc((refine_bbox[:, 2] * reg_output[:, 0]) + refine_bbox[:, 0])
        refine_bbox[:, 1] = np.trunc((refine_bbox[:, 3] * reg_output[:, 1]) + refine_bbox[:, 1])
        refine_bbox[:, 2] = np.trunc(refine_bbox[:, 2] * np.exp(reg_output[:, 2]))
        refine_bbox[:, 3] = np.trunc(refine_bbox[:, 3] * np.exp(reg_output[:, 3]))

    return refine_bbox

def BoundingBoxRegression(model, predict_bbox, img):
    # Regression Feed Forward
    results = FeedForward(model, predict_bbox, img, 4)

    # Refine Bounding box
    refine_bbox = RefineBoundingBox(predict_bbox, results)

    return refine_bbox

# Compute IOU(Measure TP, FP)
def ComputeIOU(gt_bbox, p):
    x1 = np.maximum(gt_bbox[0], p[:, 0])
    y1 = np.maximum(gt_bbox[1], p[:, 1])
    x2 = np.minimum(gt_bbox[2], p[:, 2])
    y2 = np.minimum(gt_bbox[3], p[:, 3])

    intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
    gt_area = (gt_bbox[2] - gt_bbox[0]) * (gt_bbox[3] - gt_bbox[1])
    propoesed_area = (p[:, 2] - p[:, 0]) * (p[:, 3] - p[:, 1])
    union = gt_area + propoesed_area[:] - intersection[:]

    iou = intersection/union

    return iou

# Bounding Box Normalization
def NonMaximumSuppression(boxes):
    NMS_TH = 0.5
    pick = []

    # Sorted by Score(Confidence)
    idx = np.argsort(boxes[:, 4])

    while len(idx) > 0:
        last = len(idx) - 1
        i = idx[last]
        pick.append(i)
        iou = ComputeIOU(boxes[i], boxes[idx[:last]])
        idx = np.delete(idx, np.concatenate(([last], np.where(iou > NMS_TH)[0])))

    return boxes[pick]

def DrawBoxes(img, bboxes, title='Empty', color='magenta', linestyle="solid", ax=None):
    if ax is None:
        fig, ax = plt.subplots(1, figsize=(10, 10))

    # BBox Display
    # Box 좌표 구성(xmin, ymin, xmax, ymax)
    for bbox in bboxes:
        p = patches.Rectangle((bbox[0], bbox[1]), (bbox[2]-bbox[0]), (bbox[3]-bbox[1]), linewidth=2, alpha=1.0, linestyle=linestyle, edgecolor=color, facecolor='none')
        ax.add_patch(p)

    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.axis('off')
    ax.set_title(title)