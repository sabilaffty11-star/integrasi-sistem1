from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Tugas 1 Integrasi Sistem API",
    description="API CRUD data mahasiswa terintegrasi dengan Swagger UI",
    version="1.0.0"
)

# 1. Schema Data (Model Pydantic) sesuai perintah tugas
class Mahasiswa(BaseModel):
    id: Optional[int] = None
    nama: str
    alamat: str
    ipk: float
    semester: int
    hobi: str

# Database sementara (In-Memory)
db_mahasiswa: List[Mahasiswa] = [
    Mahasiswa(id=1, nama="Salsabila", alamat="Salatiga", ipk=3.85, semester=4, hobi="Coding")
]

# 2. ENDPOINT GET (Ambil semua data)
@app.get("/mahasiswa", response_model=List[Mahasiswa], tags=["Mahasiswa"])
def get_all_mahasiswa():
    return db_mahasiswa

# 3. ENDPOINT GET (Ambil data berdasarkan ID)
@app.get("/mahasiswa/{mhs_id}", response_model=Mahasiswa, tags=["Mahasiswa"])
def get_mahasiswa_by_id(mhs_id: int):
    for mhs in db_mahasiswa:
        if mhs.id == mhs_id:
            return mhs
    raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")

# 4. ENDPOINT POST (Tambah data baru)
@app.post("/mahasiswa", response_model=Mahasiswa, status_code=201, tags=["Mahasiswa"])
def create_mahasiswa(mhs: Mahasiswa):
    new_id = len(db_mahasiswa) + 1 if db_mahasiswa else 1
    mhs.id = new_id
    db_mahasiswa.append(mhs)
    return mhs

# 5. ENDPOINT PUT (Update data)
@app.put("/mahasiswa/{mhs_id}", response_model=Mahasiswa, tags=["Mahasiswa"])
def update_mahasiswa(mhs_id: int, updated_mhs: Mahasiswa):
    for index, mhs in enumerate(db_mahasiswa):
        if mhs.id == mhs_id:
            updated_mhs.id = mhs_id
            db_mahasiswa[index] = updated_mhs
            return updated_mhs
    raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")

# 6. ENDPOINT DELETE (Hapus data)
@app.delete("/mahasiswa/{mhs_id}", tags=["Mahasiswa"])
def delete_mahasiswa(mhs_id: int):
    for index, mhs in enumerate(db_mahasiswa):
        if mhs.id == mhs_id:
            db_mahasiswa.pop(index)
            return {"message": f"Data mahasiswa dengan ID {mhs_id} berhasil dihapus"}
    raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")