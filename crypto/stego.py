import cv2 # type: ignore
import numpy as np

# ======== Helper: DCT dan Inverse DCT ========
def dct2(block):
    return cv2.dct(np.float32(block))

def idct2(block):
    return cv2.idct(block)

# ======== Fungsi: Menyisipkan data ke gambar ========
def embed_message(image_path, secret_message, output_path):
    # Baca gambar dan ubah ke grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape

    # Konversi pesan ke biner
    msg_bin = ''.join(format(ord(c), '08b') for c in secret_message)
    msg_len = len(msg_bin)
    
    # Simpan panjang pesan di 16 bit pertama lewat LSB
    img_flat = img.flatten()
    len_bin = format(msg_len, '016b')
    for i in range(16):
        img_flat[i] = (img_flat[i] & ~1) | int(len_bin[i])
    
    img = img_flat.reshape(h, w)

    # Sisipkan pesan ke dalam DCT blok 8x8
    idx = 0
    for i in range(0, h, 8):
        for j in range(0, w, 8):
            if idx >= msg_len:
                break
            block = img[i:i+8, j:j+8]
            dct_block = dct2(block)
            # Sisipkan di posisi (4,4) misal — frekuensi menengah
            bit = int(msg_bin[idx])
            coeff = int(dct_block[4][4])
            coeff = coeff & ~1 | bit
            dct_block[4][4] = coeff
            idct_block = idct2(dct_block)
            img[i:i+8, j:j+8] = idct_block
            idx += 1

    cv2.imwrite(output_path, np.uint8(img))
    print("✅ Pesan berhasil disisipkan ke", output_path)


# ======== Fungsi: Ekstraksi data ========
def extract_message(stego_path):
    img = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    img_flat = img.flatten()

    # Ambil panjang pesan dari 16 bit pertama (LSB)
    len_bits = ''.join(str(img_flat[i] & 1) for i in range(16))
    msg_len = int(len_bits, 2)

    # Ambil pesan dari DCT blok 8x8
    bits = ''
    idx = 0
    for i in range(0, h, 8):
        for j in range(0, w, 8):
            if idx >= msg_len:
                break
            block = img[i:i+8, j:j+8]
            dct_block = dct2(block)
            bit = int(dct_block[4][4]) & 1
            bits += str(bit)
            idx += 1

    # Konversi biner ke teks
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)
    return message
