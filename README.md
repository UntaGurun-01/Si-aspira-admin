# Si ASPIRA - Panel Admin (SI PENGADU)

Panel Administrasi untuk Sistem Informasi Aspirasi dan Sarana Pengaduan Informatika Responsif Akademik (Si ASPIRA) - Program Studi Teknik Informatika, Universitas Pahlawan Tuanku Tambusai.

## Fitur Utama Panel Admin
- **Dashboard Statistik & Analitik**: Rekapitulasi laporan berdasarkan status (*Baru*, *Diproses*, *Selesai*, *Ditolak*) dan grafik kategori keluhan.
- **Manajemen Pengaduan**: Detail tiket aduan, tindak lanjut status, balasan/tanggapan resmi petugas, dan log riwayat penanganan.
- **Manajemen Pengguna**: Kelola data mahasiswa dan akun staf/petugas prodi.
- **Rekap & Laporan**: Filter data pengaduan berdasarkan periode dan kategori, serta ringkasan siap cetak.
- **Pengaturan & Notifikasi**: Pengaturan profil admin, preferensi notifikasi, dan audio notifikasi kustom.

## Environment Variables di Vercel
Saat deploy ke Vercel, pastikan menambahkan Environment Variables berikut di **Project Settings > Environment Variables**:

| Variable | Contoh Nilai | Deskripsi |
|---|---|---|
| `SECRET_KEY` | `admin-panel-secret-key-pipl-2024` | Kunci sesi enkripsi Flask |
| `DATABASE_URL` | `postgresql://...` | Connection string PostgreSQL Supabase |
| `FLASK_ENV` | `production` | Mode environment Flask |

## Akun Demo Petugas / Admin
- **Username**: `admin`
- **Password**: `admin123`

## Cara Menjalankan Secara Lokal
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Jalankan server lokal (Port 5001)
python app.py
```
Akses di browser: `http://localhost:5001`
