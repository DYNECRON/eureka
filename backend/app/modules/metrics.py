filename = "data/reuters/cats.txt"


def get_metrics(query, predicted):
    truth = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('training') and query in line:

                # Extraer el número después del primer '/'
                number = line.split('/')[1].strip().split()[0]
                truth.append(number)

    true_positives = get_true_positives(predicted, truth)
    false_negatives = get_false_negatives(predicted, truth)
    false_positives = get_false_positive(predicted, truth)

    recall = true_positives / \
        (true_positives+false_negatives) if true_positives + \
        false_negatives > 0 else 0

    precision = true_positives / \
        (true_positives+false_positives) if true_positives + \
        false_positives > 0 else 0

    f1_score = (2 * true_positives) / ((2 * true_positives) +
                                       false_positives + false_negatives) if (true_positives + false_positives + false_negatives) > 0 else 0
    return recall, precision, f1_score


def get_true_positives(predicted, truth):
    true_positives = 0
    for value in predicted:
        if value in truth:
            true_positives += 1

    print("True positives", true_positives)
    return true_positives


def get_false_negatives(predicted, truth):
    set_predicted = set(predicted)
    set_verdaderos = set(truth)
    false_negatives_list = list(set_verdaderos-set_predicted)
    false_negatives = len(false_negatives_list)

    print("False negatives", false_negatives)
    return false_negatives


def get_false_positive(predicted, truth):
    set_predicted = set(predicted)
    set_verdaderos = set(truth)
    false_positives_list = list(set_predicted-set_verdaderos)
    false_positives = len(false_positives_list)
    print("False positives", false_positives)

    return false_positives
