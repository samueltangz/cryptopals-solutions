import string
import _string

# Obtain the frequency matchness of a string.
def frequency_matchness(payload, type=None):
    if type != None:
        return frequency_matchness(_string.conv(payload, type))
    # estimated_freq is obtained from https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt
    estimated_freq = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.02280148136802659, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2370624883890251, 0.0016203149830768323, 8.610900520648024e-05, 1.8321064937548985e-07, 0.0, 1.8321064937548985e-07, 3.847423636885287e-06, 0.005692171665447094, 0.00011505628780780763, 0.00011523949845718312, 1.1542270910655861e-05, 0.0, 0.015238362551156993, 0.001479242783057705, 0.014295010917522596, 9.160532468774493e-07, 5.4779984163271466e-05, 0.0001700194826204546, 6.70550976714293e-05, 6.0459514293911655e-05, 1.7038590391920558e-05, 1.5023273248790168e-05, 1.1542270910655861e-05, 7.511636624395084e-06, 7.328425975019594e-06, 0.00017368369560796437, 0.00033472585640902, 0.0031510399586090502, 8.574258390772925e-05, 1.8321064937548985e-07, 8.079589637459102e-05, 0.0019193147628576318, 1.4656851950039188e-06, 0.008150308948118043, 0.002823825738824425, 0.0039384793296249054, 0.0028732926141558073, 0.007801659082356484, 0.002145946336135113, 0.0020453636896279686, 0.003382435008770294, 0.010224253499048586, 0.00037869641225913756, 0.0011351731835305351, 0.004371039672800437, 0.0029079194268877753, 0.005008612732627142, 0.006084242455110643, 0.0021873519428939735, 0.00021582214496432706, 0.005307612512407941, 0.006231177395909786, 0.0072917838451444965, 0.0025885832650262963, 0.0006558941247642537, 0.003022242872098081, 0.00011102565352154686, 0.0016670336986675822, 9.74680654677606e-05, 0.00038199420394789636, 0.0, 0.00038052851875289246, 0.0, 1.300795610565978e-05, 1.8321064937548985e-07, 0.04482505031880485, 0.008527173253883424, 0.012217951785552668, 0.024509737462803657, 0.07413087616096008, 0.01260544230898183, 0.010449419387131065, 0.04001430508750324, 0.03630941933583208, 0.0004968672811063285, 0.00535194948955681, 0.026778251723370974, 0.017511273867309322, 0.03955957625575327, 0.05155382783841847, 0.008523875462194666, 0.00044043840109867763, 0.03827160539064358, 0.03938625898144406, 0.05312650805265767, 0.021035880339994994, 0.006227146761623525, 0.013354957075576959, 0.0008588915242722964, 0.015622555282897396, 0.00020134850366366336, 0.0, 6.045951429391165e-06, 3.664212987509797e-07, 1.8321064937548985e-07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    actual_freq = [0] * 256
    MAX_SCORE = 0
    MIN_SCORE = -(reduce((lambda x, y: x + y**2), estimated_freq) + 1)
    score = 0
    for char in payload:
        actual_freq[ord(char)] += 1
    for pos in range(256):
        actual_freq[pos] /= float(len(payload))
        score -= pow(actual_freq[pos] - estimated_freq[pos], 2)
    return (score - MIN_SCORE) / (MAX_SCORE - MIN_SCORE)

def hamming_distance(payload_1, payload_2, type=None):
    if type != None:
        return hamming_distance(
            _string.conv(payload_1, type),
            _string.conv(payload_2, type)
        )
    hamming_distance = 0
    for x, y in zip(payload_1, payload_2):
        z = ord(x) ^ ord(y)
        while z:
            hamming_distance += 1
            z -= z & (-z)
    return hamming_distance

def normalized_hamming_distance(payload_1, payload_2, type=None):
    return hamming_distance(payload_1, payload_2, type) / float(len(payload_1))