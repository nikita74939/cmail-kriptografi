def route_cipher_encrypt(plaintext, cols, clockwise=True):
    # hapus spasi dan ubah ke huruf besar
    text = ''.join(c for c in plaintext.upper() if c.isalpha())
    rows = (len(text) + cols - 1) // cols          # hitung baris yang dibutuhkan
    
    # buat grid(matrix) isi dengan baris
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
    
    # Baca spiral
    ciphertext = []
    top, bottom = 0, rows - 1
    left, right = 0, cols - 1
    
    while top <= bottom and left <= right: # cek apakah masih ada baris dan kolom
        if clockwise: #sesuai arah jam
            # kanan
            for c in range(left, right + 1):
                ciphertext.append(grid[top][c])
            top += 1
            # bawah
            for r in range(top, bottom + 1):
                ciphertext.append(grid[r][right])
            right -= 1
            # kiri (jika masih ada baris)
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    ciphertext.append(grid[bottom][c])
                bottom -= 1
            # atas (jika masih ada kolom)
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    ciphertext.append(grid[r][left])
                left += 1
        else:
            # berlawanan jarum jam (mulai dari kiri-bawah) 
            # kiri (bawah ke atas)
            for r in range(bottom, top - 1, -1):
                ciphertext.append(grid[r][left])
            left += 1
            # atas (kiri ke kanan)
            if top <= bottom:
                for c in range(left, right + 1):
                    ciphertext.append(grid[top][c])
                top += 1
            # kanan (atas ke bawah)
            if left <= right:
                for r in range(top, bottom + 1):
                    ciphertext.append(grid[r][right])
                right -= 1
            # bawah (kanan ke kiri)
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    ciphertext.append(grid[bottom][c])
                bottom -= 1
    
    return ''.join(ciphertext)


def route_cipher_decrypt(ciphertext, cols, clockwise=True):
    # ubah ke huruf besar
    text = ciphertext.upper()
    rows = (len(text) + cols - 1) // cols
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    
    # tentukan urutan pengisian spiral
    order = []
    top, bottom = 0, rows - 1
    left, right = 0, cols - 1
    
    while top <= bottom and left <= right:
        if clockwise:
            for c in range(left, right + 1):
                order.append((top, c))
            top += 1
            for r in range(top, bottom + 1):
                order.append((r, right))
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    order.append((bottom, c))
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    order.append((r, left))
                left += 1
        else:
            for r in range(bottom, top - 1, -1):
                order.append((r, left))
            left += 1
            if top <= bottom:
                for c in range(left, right + 1):
                    order.append((top, c))
                top += 1
            if left <= right:
                for r in range(top, bottom + 1):
                    order.append((r, right))
                right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    order.append((bottom, c))
                bottom -= 1
    
    # isi grid/matrix sesuai urutan spiral
    for (r, c), char in zip(order, text):
        grid[r][c] = char
    
    # baca per baris grid
    plaintext = ''
    for r in range(rows):
        for c in range(cols):
            if grid[r][c]:
                plaintext += grid[r][c]
    
    return plaintext