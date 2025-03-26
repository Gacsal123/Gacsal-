from flask import Flask, jsonify, request
import mysql.connector
from flasgger import Swagger
import mysql.connector.cursor

app = Flask(__name__)
swagger = Swagger(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'valami',
    'port': 3306
}

@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users from the database
    ---
    tags:
      - Users
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The user ID
              name:
                type: string
                description: The user's name
              email:
                type: string
                description: The user's email
      500:
        description: Database connection error
    """
    try:
        conn = mysql.connector.connect(**db_config)
        curs = conn.cursor(dictionary=True)
        curs.execute("SELECT * FROM users")
        results = curs.fetchall()
        curs.close()
        conn.close()
        return jsonify(results)
        
    except mysql.connector.Error as err:
      return jsonify({"error": f"""Csatlakozási hiba: {str(err)}"""}), 500


@app.route('/users', methods=['POST'])
def add_user():
    try:
      data = request.json
      conn = mysql.connector.connect(**db_config)
      curs = conn.cursor(dictionary=True)
      
      vezeteknev = data.get("vezeteknev", "")
      keresztnev = data.get("keresztnev", "")
      telefonszam = data.get("telefonszam", "")
      kedvenc_szin = data.get("kedvenc_szin", "")
      kedvenc_jatek = data.get("kedvenc_jatek", "")
      
      curs.execute(f"INSERT INTO users(vezeteknev, keresztnev, telefonszam, kedvenc_szin, kedvenc_jatek) VALUES ('{vezeteknev}', '{keresztnev}', '{telefonszam}','{kedvenc_szin}', '{kedvenc_jatek}')")
      
      conn.commit()
      curs.close()
      conn.close()

      return jsonify({"message":"Felhasználó sikeresen hozzáadva"}), 201
    
    except Exception as e:
        return jsonify({"error": f"Hiba történt: {str(e)}"}), 500

@app.route('/users/<int:id>', methods=['POST'])
def add_user_by_id(id):
    """
      Felhasználó hozzáadása ID alapján
      ---
      tags:
        - Users
      parameters:
        - name: id
          in: path
          required: true
          description: "A felhasználó egyedi azonosítója."
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                vezeteknev:
                  type: string
                  description: "A felhasználó vezetékneve."
                keresztnev:
                  type: string
                  description: "A felhasználó keresztneve."
                telefonszam:
                  type: string
                  description: "A felhasználó telefonszáma."
                kedvenc_szin:
                  type: string
                  description: "A felhasználó kedvenc színe."
                kedvenc_jatek:
                  type: string
                  description: "A felhasználó kedvenc játéka."
      responses:
        201:
          description: "Felhasználó sikeresen hozzáadva."
          schema:
            type: object
            properties:
              message:
                type: string
                example: "Felhasználó sikeresen hozzáadva"
        500:
          description: "Hiba történt a kérés feldolgozása közben."
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Hiba történt: adatbázis hiba"
      """
    try:
      data = request.json
      conn = mysql.connector.connect(**db_config)
      curs = conn.cursor(dictionary=True)

      vezeteknev = data.get("vezeteknev", "")
      keresztnev = data.get("keresztnev", "")
      telefonszam = data.get("telefonszam", "")
      kedvenc_szin = data.get("kedvenc_szin", "")
      kedvenc_jatek = data.get("kedvenc_jatek", "")
      
      curs.execute(f"INSERT INTO users(ID, vezeteknev, keresztnev, telefonszam, kedvenc_szin, kedvenc_jatek) VALUES ('{id}', '{vezeteknev}', '{keresztnev}', '{telefonszam}','{kedvenc_szin}', '{kedvenc_jatek}')")
      
      conn.commit()
      curs.close()
      conn.close()

      return jsonify({"message":"Felhasználó sikeresen hozzáadva"}), 201
    
    except mysql.connector.Error as err:
      return jsonify({"error": f"Hiba történt: {str(err)}"})


    except Exception as e:
        return jsonify({"error": f"Hiba történt: {str(e)}"}), 500


@app.route('/users/<int:id>', methods=['PUT'])
def update_user_by_id(id):
    """
      Felhasználó frissítése ID alapján
      ---
      tags:
        - Users
      parameters:
        - name: id
          in: path
          required: true
          description: "A felhasználó egyedi azonosítója."
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                vezeteknev:
                  type: string
                  description: "A felhasználó vezetékneve."
                keresztnev:
                  type: string
                  description: "A felhasználó keresztneve."
                telefonszam:
                  type: string
                  description: "A felhasználó telefonszáma."
                kedvenc_szin:
                  type: string
                  description: "A felhasználó kedvenc színe."
                kedvenc_jatek:
                  type: string
                  description: "A felhasználó kedvenc játéka."
      responses:
        200:
          description: "Felhasználó sikeresen frissítve."
          schema:
            type: object
            properties:
              message:
                type: string
                example: "Felhasználó sikeresen frissítve"
        500:
          description: "Hiba történt a kérés feldolgozása közben."
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Hiba történt: adatbázis hiba"
    """
    try:
        data = request.json
        conn = mysql.connector.connect(**db_config)
        curs = conn.cursor(dictionary=True)

        vezeteknev = data.get("vezeteknev", "")
        keresztnev = data.get("keresztnev", "")
        telefonszam = data.get("telefonszam", "")
        kedvenc_szin = data.get("kedvenc_szin", "")
        kedvenc_jatek = data.get("kedvenc_jatek", "")

        curs.execute(f"""
            UPDATE users 
            SET vezeteknev = '{vezeteknev}', 
                keresztnev = '{keresztnev}', 
                telefonszam = '{telefonszam}', 
                kedvenc_szin = '{kedvenc_szin}', 
                kedvenc_jatek = '{kedvenc_jatek}' 
            WHERE ID = {id}
        """)

        conn.commit()
        curs.close()
        conn.close()

        return jsonify({"message": "Felhasználó sikeresen frissítve"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Hiba történt: {str(err)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Hiba történt: {str(e)}"}), 500


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user_by_id(id):
    """
      Felhasználó törlése ID alapján
      ---
      tags:
        - Users
      parameters:
        - name: id
          in: path
          required: true
          description: "A felhasználó egyedi azonosítója."
          schema:
            type: integer
      responses:
        204:
          description: "Felhasználó sikeresen törölve."
        500:
          description: "Hiba történt a kérés feldolgozása közben."
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Hiba történt: adatbázis hiba"
    """
    try:
        conn = mysql.connector.connect(**db_config)
        curs = conn.cursor(dictionary=True)

        curs.execute(f"DELETE FROM users WHERE ID = {id}")

        conn.commit()
        curs.close()
        conn.close()

        return jsonify({"message": "Felhasználó sikeresen törölve"}), 204

    except mysql.connector.Error as err:
        return jsonify({"error": f"Hiba történt: {str(err)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Hiba történt: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)