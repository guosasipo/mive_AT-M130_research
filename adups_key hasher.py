import hashlib
import random

def encode_data(s: str) -> str:
    data = bytes(s, 'utf8')

    useless_bytes_num = random.randint(0, 14)
    random_bytes_num = random.randint(0, 11) + 3
    random_bytes = bytes(
        [random.randint(0, 254) for _ in range(random_bytes_num)]
    )

    # Encode data with random_bytes
    data = bytes(
        [(data[i] ^ random_bytes[i % random_bytes_num]) for i in range(len(data))]
    )

    # Shift random_bytes
    shifted_bytes = bytes(
        [((random_bytes[i] >> 5) | ((random_bytes[i] << 3) % 255)) for i in range(len(random_bytes))]
    )

    # Add amount of useless bytes & random bytes
    out_bytes = [random_bytes_num | (useless_bytes_num << 4)]
    # Add useless bytes
    if useless_bytes_num > 0:
        for _ in range(useless_bytes_num):
            out_bytes.append(0)
        out_bytes[1] = 8
    # Add shifted random bytes
    for b in shifted_bytes:
        out_bytes.append(b)
    # Add encoded data
    for b in data:
        out_bytes.append(b)

    out = ''
    for b in out_bytes:
        out += f'{b:02x}'

    return out.upper()

def decode_data(key: str) -> str:
    data: bytearray = bytearray.fromhex(key)

    useless_bytes_num = data[0] >> 4
    assert 0 <= useless_bytes_num <= 14
    random_bytes_num = data[0] & 0xf
    assert 3 <= random_bytes_num <= 14
    data = data[1:]

    # Check & remove useless bytes
    if useless_bytes_num > 0:
        assert data[0] == 8
        for i in range(1, useless_bytes_num):
            assert data[i] == 0
    data = data[useless_bytes_num:]

    # Unshift & remove random bytes
    random_bytes = []
    for i in range(random_bytes_num):
        random_bytes.append(
            (255 * (data[i] & 0x7) + data[i]) >> 3
        )

        assert 0 <= random_bytes[i] <= 254
    data = data[random_bytes_num:]

    # Decode data
    for i in range(len(data)):
        data[i] = data[i] ^ random_bytes[i % random_bytes_num]

    return data.decode('utf8')

def calculate_sha_key(data: str) -> str:
    hash = hashlib.sha256()
    hash.update(bytes(data, 'utf8'))
    return hash.hexdigest()

def generate_post_data(config: dict[str, str]) -> str:
    data = ''
    for key, value in config.items():
        data += f'&{key}={value}'

    data = encode_data(data)
    return f'key={data}&shaKey={calculate_sha_key(data)}'

def main():
    parameter_str = "&appCode=0&project=lens$MSM$13.0_AT-M130-KT_en-US_other&version=AT-M130KX0201T"
    encode_str = encode_data(parameter_str)
    # 315 ~ lensdown
    print("Encoded Data:")
    print(encode_str)
    # POST to https://fota5p.adups.com/otainter-5.0/fota5/detectSchedule.do parameter key


if __name__ == '__main__':
    main()