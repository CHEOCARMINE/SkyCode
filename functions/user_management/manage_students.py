from flask import Blueprint, request, jsonify, redirect, url_for, flash
from database import db
from models import Alumno

manage_students = Blueprint('manage_students', __name__)

@manage_students.route('/alumnos', methods=['POST'])
def crear_alumno():
    data = request.form
    usuario_id = data.get('usuario_id')
    if not usuario_id or usuario_id == '':
        usuario_id = 1  # Valor predeterminado válido para `usuario_id`
    nuevo_alumno = Alumno(
        usuario_id=usuario_id,
        matricula=data['matricula'],
        nombre=data['nombre'],
        domicilio=data.get('domicilio', ''),
        telefono=data.get('telefono', ''),
        correo_electronico=data['correo_electronico'],
        estatus=data.get('estatus', 'Activo'),
        carrera=data['carrera']
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    flash('Alumno creado con éxito', 'success')
    return redirect(url_for('agregar_alumno'))

@manage_students.route('/alumnos', methods=['GET'])
def obtener_alumnos():
    alumnos = Alumno.query.all()
    output = []
    for alumno in alumnos:
        alumno_data = {
            'id': alumno.id,
            'usuario_id': alumno.usuario_id,
            'matricula': alumno.matricula,
            'nombre': alumno.nombre,
            'domicilio': alumno.domicilio,
            'telefono': alumno.telefono,
            'correo_electronico': alumno.correo_electronico,
            'estatus': alumno.estatus,
            'carrera': alumno.carrera
        }
        output.append(alumno_data)
    return jsonify({"alumnos": output})

@manage_students.route('/alumnos/<id>', methods=['PUT'])
def actualizar_alumno(id):
    data = request.get_json()
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    alumno.usuario_id = data['usuario_id']
    alumno.matricula = data['matricula']
    alumno.nombre = data['nombre']
    alumno.domicilio = data['domicilio']
    alumno.telefono = data['telefono']
    alumno.correo_electronico = data['correo_electronico']
    alumno.estatus = data['estatus']
    alumno.carrera = data['carrera']

    db.session.commit()
    return jsonify({"mensaje": "Alumno actualizado con éxito"})

@manage_students.route('/alumnos/<id>', methods=['DELETE'])
def eliminar_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"mensaje": "Alumno eliminado con éxito"})
