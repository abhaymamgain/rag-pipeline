from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cfg
import query
import populate_db


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = cfg.PATH
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No file part'})
    files = request.files.getlist('files[]')
    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file:
            
            filename = file.filename
            file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.isfile(file_path):
              file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            populate_db.fill_db()
            
    return jsonify({'success': True, 'message': 'Files uploaded successfully'})


@app.route('/gen_res',methods=['POST'])
def gen_res():
    try:
        
        data = request.get_json()
        input_text=data.get('input_text')
        generated=query.query_rag(input_text)
        return jsonify({"generated_text": generated})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/cleardb',methods=['POST'])
def cleardb():
    # populate_db.clear_database()
    delete_files_in_folder(cfg.PATH)
    return jsonify({'success': True, 'message': 'cleared successfully'})

def delete_files_in_folder(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    # Iterate over each file and delete it
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")

# Specify the folder path
  
if __name__ == '__main__':
    app.run(debug=True)
