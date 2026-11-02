import pypandoc

content = r"""# System Architecture — Lab Equipment Loan System

## 1. Overview

Lab Equipment Loan System adalah aplikasi backend untuk mengelola data alat laboratorium, transaksi peminjaman, pengembalian alat, dan riwayat peminjaman mahasiswa. Sistem menyediakan REST API dengan format pertukaran data JSON.

Arsitektur menggunakan pendekatan **layered architecture** agar tanggung jawab setiap bagian aplikasi terpisah dan mudah dipelihara.

## 2. Technology Stack

| Komponen | Teknologi |
|---|---|
| Bahasa pemrograman | Python 3.x |
| Backend framework | Flask |
| Database | SQLite |
| Format pertukaran data | JSON |
| Antarmuka API | REST API |

FastAPI tidak digunakan. Flask menjadi framework backend utama.

## 3. Architecture Style

Sistem menggunakan **layered architecture** dengan tiga lapisan utama:

1. **API / Presentation Layer** — menerima HTTP request, memvalidasi input dasar, dan mengirimkan response JSON.
2. **Service / Business Logic Layer** — menjalankan aturan peminjaman, pengembalian, validasi stok, dan perubahan status transaksi.
3. **Data Access Layer** — berinteraksi dengan database SQLite untuk membaca dan menyimpan data `Item` dan `Loan`.

### 3.1 Architecture Diagram

```text
Client (Mahasiswa / Petugas Lab)
              |
              | HTTP Request / JSON
              v
       Flask REST API
              |
              v
      API / Route Layer
              |
              v
    Service / Business Logic
       |              |
       |              +-- Validasi transaksi
       |              +-- Pemeriksaan stok
       |              +-- Perubahan status
       v
       Data Access Layer
              |
              v
         SQLite DB
          |      |
          v      v
         Item   Loan

Flask REST API
      |
      | HTTP Response / JSON
      v
Client (Mahasiswa / Petugas Lab)
```

## 4. Component Responsibilities

### 4.1 API / Route Layer

Bertanggung jawab untuk:
- Menyediakan endpoint sesuai kebutuhan sistem.
- Membaca parameter, path variable, dan request body.
- Melakukan validasi format input dasar.
- Memanggil fungsi pada service layer.
- Mengembalikan HTTP status code dan response JSON yang sesuai.

Endpoint yang disediakan:

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/items` | Menampilkan daftar alat dan stok terkini. |
| POST | `/items` | Menambahkan master data alat. |
| POST | `/loans` | Mencatat pengajuan peminjaman alat. |
| PUT | `/loans/{id}/return` | Memproses pengembalian alat. |
| GET | `/loans/student/{student_id}` | Menampilkan riwayat peminjaman berdasarkan NIM. |

### 4.2 Service / Business Logic Layer

Bertanggung jawab untuk menjalankan aturan bisnis.

**Proses peminjaman:**
1. Menerima `student_id`, `item_id`, dan `quantity`.
2. Memastikan alat dengan `item_id` tersedia.
3. Memastikan `quantity` merupakan bilangan bulat positif.
4. Memastikan `quantity` tidak melebihi `available_stock`.
5. Mengurangi `available_stock` sesuai jumlah yang dipinjam.
6. Membuat transaksi dengan status `BORROWED`.
7. Menyimpan perubahan stok dan transaksi secara atomik.

**Proses pengembalian:**
1. Mencari transaksi berdasarkan ID.
2. Memastikan transaksi ditemukan.
3. Memastikan status transaksi belum `RETURNED`.
4. Mengubah status transaksi menjadi `RETURNED`.
5. Menambahkan kembali jumlah pinjaman ke `available_stock`.
6. Menyimpan perubahan status dan stok secara atomik.

Transaksi yang sudah berstatus `RETURNED` tidak boleh diproses kembali agar stok tidak bertambah ganda.

### 4.3 Data Access Layer

Bertanggung jawab untuk:
- Membuat koneksi ke SQLite.
- Menjalankan operasi query dan perubahan data.
- Mengelola penyimpanan data `Item` dan `Loan`.
- Menggunakan parameterized query untuk mengurangi risiko SQL injection.
- Mengelola commit dan rollback transaksi database.

## 5. Database Architecture

Sistem menggunakan SQLite sebagai relational database dengan dua tabel utama.

### 5.1 Entity: Item

| Field | Type | Constraint / Description |
|---|---|---|
| `id` | INTEGER | Primary Key |
| `name` | TEXT | NOT NULL |
| `total_stock` | INTEGER | Jumlah stok keseluruhan |
| `available_stock` | INTEGER | Jumlah stok yang tersedia |

### 5.2 Entity: Loan

| Field | Type | Constraint / Description |
|---|---|---|
| `id` | INTEGER | Primary Key |
| `student_id` | TEXT | NIM mahasiswa |
| `item_id` | INTEGER | Foreign Key ke `Item.id` |
| `quantity` | INTEGER | Jumlah alat yang dipinjam |
| `status` | TEXT | `BORROWED`, `RETURNED`, atau `CANCELLED` |
| `created_at` | TIMESTAMP | Waktu transaksi dibuat |

### 5.3 Entity Relationship

```text
+-------------------+          +-------------------+
|       Item        |          |       Loan        |
+-------------------+          +-------------------+
| PK id             |<-------- | PK id             |
| name              |    1 : N | student_id        |
| total_stock       |          | FK item_id        |
| available_stock   |          | quantity          |
+-------------------+          | status            |
                               | created_at        |
                               +-------------------+
```

Satu data `Item` dapat memiliki banyak transaksi `Loan`, sedangkan setiap transaksi `Loan` mengacu pada satu data `Item`.

Relasi menggunakan `Loan.item_id` sebagai foreign key yang mengacu pada `Item.id`.

## 6. Data Flow

### 6.1 Menampilkan Daftar Alat

1. Client mengirim `GET /items`.
2. Route layer meminta data alat kepada data access layer.
3. Database mengembalikan data alat.
4. API mengirim daftar alat beserta `total_stock` dan `available_stock` dalam format JSON.

### 6.2 Menambahkan Data Alat

1. Petugas Lab mengirim `POST /items` dengan nama alat dan jumlah stok awal.
2. API memvalidasi input.
3. Service memastikan nilai stok valid.
4. Data alat disimpan ke tabel `Item`.
5. API mengembalikan response `201 Created` jika berhasil.

### 6.3 Mengajukan Peminjaman

1. Mahasiswa mengirim `POST /loans` dengan NIM, ID alat, dan jumlah pinjaman.
2. API memvalidasi input.
3. Service memeriksa keberadaan alat dan ketersediaan stok.
4. Jika stok mencukupi, sistem mengurangi `available_stock` dan membuat transaksi berstatus `BORROWED`.
5. Kedua perubahan disimpan dalam satu transaksi database.
6. API mengembalikan `201 Created`.

Jika alat tidak ditemukan, API mengembalikan `404 Not Found`. Jika jumlah pinjaman melebihi stok tersedia, API mengembalikan `400 Bad Request`.

### 6.4 Mengembalikan Alat

1. Client mengirim `PUT /loans/{id}/return`.
2. Service mencari transaksi peminjaman.
3. Service memeriksa status transaksi.
4. Jika status masih `BORROWED`, sistem mengubah status menjadi `RETURNED` dan memulihkan stok.
5. Kedua perubahan disimpan dalam satu transaksi database.
6. API mengembalikan `200 OK`.

Jika transaksi tidak ditemukan, API mengembalikan `404 Not Found`. Jika transaksi sudah `RETURNED`, API mengembalikan `400 Bad Request`.

### 6.5 Melihat Riwayat Peminjaman

1. Client mengirim `GET /loans/student/{student_id}`.
2. API meneruskan NIM ke service.
3. Data access layer mengambil transaksi berdasarkan `student_id`.
4. API mengembalikan daftar riwayat peminjaman dalam format JSON.

## 7. Business Rules and Data Integrity

Aturan berikut harus dijaga oleh service layer dan database:

- `quantity` harus berupa bilangan bulat positif.
- `total_stock` dan `available_stock` tidak boleh bernilai negatif.
- `available_stock` tidak boleh melebihi `total_stock`.
- Peminjaman hanya berhasil jika stok tersedia mencukupi.
- Stok berkurang saat transaksi peminjaman berhasil dicatat.
- Pengembalian hanya dapat dilakukan pada transaksi yang belum berstatus `RETURNED`.
- Pengembalian menambah stok sesuai `quantity` transaksi.
- Perubahan stok dan status transaksi harus dilakukan dalam satu transaksi database.
- Kegagalan salah satu proses harus menyebabkan rollback agar data tetap konsisten.
- Pemeriksaan dan perubahan stok perlu dilakukan secara aman untuk mencegah dua peminjaman bersamaan menggunakan stok yang sama.

## 8. Error Handling and HTTP Response

| Kondisi | HTTP Status |
|---|---|
| Request berhasil mengambil data | `200 OK` |
| Data berhasil dibuat | `201 Created` |
| Input tidak valid atau stok tidak mencukupi | `400 Bad Request` |
| Data alat atau transaksi tidak ditemukan | `404 Not Found` |
| Kesalahan internal server | `500 Internal Server Error` |

Response error menggunakan format JSON yang konsisten, misalnya:

```json
{
  "error": "Insufficient stock",
  "message": "Jumlah peminjaman melebihi stok yang tersedia."
}
```

## 9. Suggested Project Structure

```text
lab-equipment-loan-system/
|
+-- app/
|   +-- __init__.py
|   +-- routes/
|   |   +-- item_routes.py
|   |   +-- loan_routes.py
|   |
|   +-- services/
|   |   +-- item_service.py
|   |   +-- loan_service.py
|   |
|   +-- repositories/
|   |   +-- item_repository.py
|   |   +-- loan_repository.py
|   |
|   +-- database/
|       +-- connection.py
|       +-- schema.sql
|
+-- tests/
|   +-- test_items.py
|   +-- test_loans.py
|
+-- instance/
|   +-- lab_loan.db
|
+-- run.py
+-- requirements.txt
+-- architecture.md
+-- README.md
```

Struktur ini merupakan rekomendasi pemisahan kode. Nama file atau folder dapat disesuaikan saat implementasi tanpa mengubah tanggung jawab arsitektur.

## 10. Security and Non-Functional Considerations

- Gunakan parameterized query untuk seluruh input database.
- Validasi semua input dari client sebelum diproses.
- Jangan mengembalikan detail internal database atau stack trace kepada client.
- Aktifkan foreign key constraint SQLite.
- Gunakan transaksi database untuk operasi yang mengubah stok dan status.
- Simpan konfigurasi dan file database pada lokasi yang tidak dapat diakses langsung melalui endpoint publik.
- Pastikan response API menggunakan JSON dengan struktur yang konsisten.

Autentikasi, otorisasi, dan pembagian hak akses pengguna belum didefinisikan dalam SRS dan PRD saat ini. Implementasinya memerlukan requirement tambahan.

## 11. Assumptions and Scope

- Sistem berfokus pada backend REST API.
- Mahasiswa diidentifikasi menggunakan NIM (`student_id`).
- Petugas Lab bertanggung jawab menambahkan master data alat.
- Status transaksi yang didefinisikan adalah `BORROWED`, `RETURNED`, dan `CANCELLED`.
- Endpoint pembatalan transaksi belum termasuk dalam daftar endpoint yang ditentukan.
- Belum ada ketentuan tanggal jatuh tempo, denda, persetujuan petugas, maupun autentikasi pengguna.
- Pengembalian dilakukan untuk seluruh jumlah dalam satu transaksi karena endpoint dan aturan yang tersedia belum mendefinisikan pengembalian sebagian.

---

**Document:** `architecture.md`  
**System:** Lab Equipment Loan System  
**Backend Framework:** Flask  
**Database:** SQLite  
**API Format:** JSON
"""

output_path = "/mnt/data/architecture.md"
pypandoc.convert_text(content, "md", format="md", outputfile=output_path, extra_args=["--standalone"])
print(f"Created: {output_path}")
