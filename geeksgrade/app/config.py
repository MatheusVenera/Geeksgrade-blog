class Config:

    SECRET_KEY = "m76ujy5"
    #Chave de criptografia

    SQLALCHEMY_DATABASE_URI = 'sqlite:///geekgrades.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = '/home/aluno/Downloads/geeksgrade/app/static/images/'
    #Mudar toda vez