from scipy import spatial
from decimal import Decimal, ROUND_HALF_UP


# noinspection PyShadowingNames
def read_input():
    N, M = [int(x) for x in input().strip().split(' ')]
    ratings = []
    for _ in range(N):
        ratings.append([0 if g == 'X' else int(g) for g in input().strip().split(' ')])
    Q = int(input().strip())
    queries = []
    for _ in range(Q):
        queries.append([int(q) for q in input().strip().split(' ')])
    return N, M, ratings, queries


def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


# noinspection PyShadowingNames
def normalize(ratings):
    for i in range(len(ratings)):
        mean = sum(ratings[i]) / sum([1 for rating in ratings[i] if rating != 0])
        for j in range(len(ratings[0])):
            if ratings[i][j] > 0:
                ratings[i][j] -= mean
    return ratings


# noinspection PyShadowingNames
def pearson_similarities(ratings, N, M):
    normalized_ratings = [normalize([[ratings[x][y] for y in range(M)] for x in range(N)]),
                          normalize(transpose([[ratings[x][y] for y in range(M)] for x in range(N)]))]
    similarities = dict()
    similarities[0] = []
    similarities[1] = []
    for i in range(N - 1):
        for j in range(i + 1, N):
            similarity = 1 - spatial.distance.cosine(normalized_ratings[0][i], normalized_ratings[0][j])
            if similarity > 0:
                similarities[0].append((similarity, (i, j)))

    for i in range(M - 1):
        for j in range(i + 1, M):
            similarity = 1 - spatial.distance.cosine(normalized_ratings[1][i], normalized_ratings[1][j])
            if similarity > 0:
                similarities[1].append((similarity, (i, j)))
    similarities[0].sort(reverse=True)
    similarities[1].sort(reverse=True)
    return similarities


# noinspection PyShadowingNames
def CF(N, M, ratings, queries):
    similarities = pearson_similarities(ratings, N, M)
    for I, J, T, K in queries:
        I -= 1
        J -= 1

        similarities_w_o_zeros = []
        if T == 0:
            for similarity in similarities[T]:
                if similarity[1][0] == I:
                    if ratings[similarity[1][1]][J] != 0:
                        similarities_w_o_zeros.append(similarity)
                if similarity[1][1] == I:
                    if ratings[similarity[1][0]][J] != 0:
                        similarities_w_o_zeros.append(similarity)
        else:
            for similarity in similarities[T]:
                if similarity[1][0] == J:
                    if ratings[I][similarity[1][1]] != 0:
                        similarities_w_o_zeros.append(similarity)
                if similarity[1][1] == J:
                    if ratings[I][similarity[1][0]] != 0:
                        similarities_w_o_zeros.append(similarity)

        weighted_ratings = 0
        similarities_sum = 0

        if T == 0:
            for similarity in [s for s in similarities_w_o_zeros if s[1][0] == I or s[1][1] == I][:K]:
                similarities_sum += similarity[0]
                if similarity[1][0] == I:
                    weighted_ratings += similarity[0] * ratings[similarity[1][1]][J]
                else:
                    weighted_ratings += similarity[0] * ratings[similarity[1][0]][J]
        else:
            for similarity in [s for s in similarities_w_o_zeros if s[1][0] == J or s[1][1] == J][:K]:
                similarities_sum += similarity[0]
                if similarity[1][0] == J:
                    weighted_ratings += similarity[0] * ratings[I][similarity[1][1]]
                else:
                    weighted_ratings += similarity[0] * ratings[I][similarity[1][0]]

        print(Decimal(Decimal(weighted_ratings / similarities_sum).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)))


if __name__ == '__main__':
    N, M, ratings, queries = read_input()
    CF(N, M, ratings, queries)
