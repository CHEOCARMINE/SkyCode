from flask import Flask, request, jsonify, render_template, redirect, url_for
from database import db, app
from models import Alumno

# Ruta para mostrar la lista de alumnos en HTML
@app.route('/alumnos_web')
def alumnos_web():
    alumnos = Alumno.query.all()
    return render_template('alumnos.html', alumnos=alumnos)

# Ruta para obtener todos los alumnos en JSON
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    alumnos = Alumno.query.all()
    alumnos_list = [{"id": a.id, "matricula": a.matricula, "nombre": a.nombre,
                     "domicilio": a.domicilio, "telefono": a.telefono, 
                     "correo": a.correo_electronico, "estatus": a.estatus, 
                     "carrera": a.carrera} for a in alumnos]
    return jsonify(alumnos_list)

# Ruta para agregar un nuevo alumno
@app.route('/alumnos', methods=['POST'])
def add_alumno():
    data = request.json
    nuevo_alumno = Alumno(
        usuario_id=data['usuario_id'],
        matricula=data['matricula'],
        nombre=data['nombre'],
        domicilio=data['domicilio'],
        telefono=data['telefono'],
        correo_electronico=data['correo_electronico'],
        estatus=data['estatus'],
        carrera=data['carrera']
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    return jsonify({"mensaje": "Alumno agregado correctamente"}), 201

# Ruta para eliminar un alumno
@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"mensaje": "Alumno no encontrado"}), 404
    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"mensaje": "Alumno eliminado correctamente"})

# Ruta para actualizar un alumno
@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"mensaje": "Alumno no encontrado"}), 404
    data = request.json
    alumno.matricula = data['matricula']
    alumno.nombre = data['nombre']
    alumno.domicilio = data['domicilio']
    alumno.telefono = data['telefono']
    alumno.correo_electronico = data['correo_electronico']
    alumno.estatus = data['estatus']
    alumno.carrera = data['carrera']
    db.session.commit()
    return jsonify({"mensaje": "Alumno actualizado correctamente"})

