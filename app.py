from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    history = """
    <h1>Les débuts d'Internet</h1>
    <p>
        Internet a commencé dans les années 1960 avec ARPANET, un projet de recherche du Département de la Défense américain.
    </p>
    <h2>Dates clés :</h2>
    <ul>
        <li><strong>1969</strong> : Premier message envoyé sur ARPANET entre l'UCLA et le Stanford Research Institute</li>
        <li><strong>1971</strong> : Ray Tomlinson invente le courrier électronique (@)</li>
        <li><strong>1974</strong> : Développement du protocole TCP/IP</li>
        <li><strong>1983</strong> : Adoption officielle du protocole TCP/IP</li>
        <li><strong>1989</strong> : Tim Berners-Lee invente le World Wide Web (WWW) au CERN</li>
        <li><strong>1991</strong> : Premier site web mis en ligne</li>
        <li><strong>1995</strong> : Début de l'ère commerciale d'Internet</li>
    </ul>
    <p>
        Ces innovations ont transformé la façon dont les gens communiquent, travaillent et partagent les informations dans le monde entier.
    </p>
    <h1>Green Boys</h1>
    """
    return history

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
