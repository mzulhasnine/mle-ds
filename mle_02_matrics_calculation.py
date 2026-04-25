def precision_recall_f1(y_true, y_pred):

    # +ve is 1, -ve is 0

    tp = sum(a==1 and b==1 for a,b in zip(y_true, y_pred))
    # tn = sum(a==0 and b==0 for a,b in zip(y_true, y_pred))
    fp = sum(a==0 and b==1 for a,b in zip(y_true, y_pred))
    fn = sum(a==1 and b==0 for a,b in zip(y_true, y_pred))


    # tp = fp = fn = tn = 0

    # for i in range(len(y_true)):
    #     if y_true[i] == 1 and y_pred[i] == 1:
    #         tp += 1
    #     elif y_true[i] == 0 and y_pred[i] == 1:
    #         fp += 1
    #     elif y_true[i] == 1 and y_pred[i] == 0:
    #         fn += 1
    #     elif y_true[i] == 0 and y_pred[i] == 0:
    #         tn += 1


    recall = tp/ (tp + fn) if tp + fn > 0 else 0
    precision = tp/ (tp + fp) if tp + fp > 0 else 0
    f1 = 2*recall*precision / (precision + recall) if precision + recall > 0 else 0

    return precision, recall, f1


if __name__ == "__main__":

    y_true = [1, 0, 1, 1, 0, 1, 1, 1]
    y_pred = [1, 1, 1, 0, 0, 1, 1, 0]

    p, r, f1 = precision_recall_f1(y_true, y_pred)

    print("Precision:", round(p, 3))
    print("Recall:", round(r, 3))
    print("F1:", round(f1, 3))