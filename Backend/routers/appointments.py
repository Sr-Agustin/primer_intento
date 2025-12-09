from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend import schemas, crud_appointments
from Backend.auth_utils import get_current_user

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
    
)


# Crear turno (requiere usuario autenticado)
@router.post("/", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return crud_appointments.create_appointment(db, current_user.id, appointment)


# Listar todos los turnos
@router.get("/", response_model=list[schemas.AppointmentResponse])
def get_all_appointments(db: Session = Depends(get_db)):
    return crud_appointments.get_all_appointments(db)


# Listar turnos del usuario autenticado
@router.get("/me", response_model=list[schemas.AppointmentResponse])
def get_my_appointments(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return crud_appointments.get_user_appointments(db, current_user.id)


# Cambiar estado del turno
@router.patch("/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment_status(
    appointment_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    appointment = crud_appointments.update_appointment_status(db, appointment_id, status)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


# Borrar turno
@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = crud_appointments.delete_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted"}
