from flask import Flask, request, redirect, url_for
import numpy as np

app = Flask(__name__)

# Constantes pour le calcul
D_exp = 1.33e-5  # Valeur expérimentale pour l'erreur
lambda_A = 1.127
lambda_B = 0.973
q_A = 1.432
q_B = 1.4
theta_A = 0.388
theta_B = 0.739
theta_BA = 0.612
theta_AB = 0.261
theta_AA = 0.388
theta_BB = 0.739
tau_AB = 1.035
tau_BA = 0.5373

# Fonction pour calculer le coefficient de diffusion et l'erreur
def compute_diffusion_coefficient(x_A, D_AB_0_A, D_AB_0_B, D_exp):
    # Calcul de x_B
    x_B = 1 - x_A
    # Calcul des paramètres UNIFAC
    phi_A = x_A * lambda_A / (x_A * lambda_A + x_B * lambda_B)
    phi_B = x_B * lambda_B / (x_A * lambda_A + x_B * lambda_B)

    # Calcul des termes de l'équation
    term1 = x_B * np.log(D_AB_0_A) + x_A * np.log(D_AB_0_B)
    term2 = 2 * (x_A * np.log(x_A / phi_A) + x_B * np.log(x_B / phi_B))
    term3 = 2 * x_A * x_B * ((phi_A / x_A) * (1 - (lambda_A / lambda_B)) + (phi_B / x_B) * (1 - (lambda_B / lambda_A)))
    term4 = (x_B * q_A) * ((1 - theta_BA**2) * np.log(tau_BA) + (1 - theta_BB**2) * tau_AB * np.log(tau_AB))
    term5 = (x_A * q_B) * ((1 - theta_AB**2) * np.log(tau_AB) + (1 - theta_AA**2) * tau_BA * np.log(tau_BA))
    # Calcul de ln(D_AB) et D_AB
    ln_D_AB = term1 + term2 + term3 + term4 + term5
    D_AB = np.exp(ln_D_AB)

    # Calcul de l'erreur
    error = abs((D_AB - D_exp) / D_exp) * 100

    return D_AB, error

# Page 1: Accueil
@app.route('/')
def home():
    return """
        <html>
            <head>
                <title>Accueil - Calculateur de Diffusion</title>
            </head>
            <body>
                <h1 style="text-align: center;">Bienvenue, je suis Amine Chrouii</h1>
                <p style="text-align: center;">Je suis étudiant en PIC 12</p>
                <p style="text-align: center;">Bienvenue dans le calculateur du coefficient de diffusion.</p>
                <div style="text-align: center;">
                    <a href='/page2'><button>Aller au formulaire</button></a>
                </div>
            </body>
        </html>
    """

# Page 2: Formulaire d'entrée
@app.route('/page2', methods=['GET'])
def page2():
    return """
        <html>
            <head>
                <title>Formulaire de calcul</title>
            </head>
            <body>
                <h1 style="text-align: center;">Entrez les variables et leurs valeurs</h1>
                <form action='/page3' method='post'>
                    <div style="display: flex; justify-content: center; flex-wrap: wrap;">
                        <div style="margin: 10px;">
                            Fraction molaire de A (x_A): <input type='text' name='x_A' value='0.25' required><br><br>
                            Coefficient de diffusion initial D_AB_0_A: <input type='text' name='D_AB_0_A' value='2.1e-5' required><br><br>
                            Phi A (φ_A): <input type='text' name='phi_A' value='0.279' required><br><br>
                            Lambda A (λ_A): <input type='text' name='lambda_A' value='1.127' required><br><br>
                            Theta BA (θ_BA): <input type='text' name='theta_BA' value='0.612' required><br><br>
                            Theta AA (θ_AA): <input type='text' name='theta_AA' value='0.388' required><br><br>
                        </div>
                        <div style="margin: 10px;">
                            Coefficient de diffusion initial D_AB_0_B: <input type='text' name='D_AB_0_B' value='2.67e-5' required><br><br>
                            Phi B (φ_B): <input type='text' name='phi_B' value='0.746' required><br><br>
                            Lambda B (λ_B): <input type='text' name='lambda_B' value='0.973' required><br><br>
                            Theta AB (θ_AB): <input type='text' name='theta_AB' value='0.261' required><br><br>
                            Theta BB (θ_BB): <input type='text' name='theta_BB' value='0.739' required><br><br>
                            Tau AB (τ_AB): <input type='text' name='tau_AB' value='1.035' required><br><br>
                            Tau BA (τ_BA): <input type='text' name='tau_BA' value='0.5373' required><br><br>
                            q_A: <input type='text' name='q_A' value='1.432' required><br><br>
                            q_B: <input type='text' name='q_B' value='1.4' required><br><br>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <button type='submit'>Calculer</button>
                    </div>
                </form>
            </body>
        </html>
    """

# Page 3: Résultat du calcul
@app.route('/page3', methods=['POST'])
def page3():
    try:
        x_A = float(request.form['x_A'].replace(',', '.'))
        D_AB_0_A = float(request.form['D_AB_0_A'])
        D_AB_0_B = float(request.form['D_AB_0_B'])

        D_AB, error = compute_diffusion_coefficient(x_A, D_AB_0_A, D_AB_0_B, D_exp)
        
        return f"""
            <html>
                <head>
                    <title>Résultat du calcul</title>
                </head>
                <body>
                    <h1 style="text-align: center;">Résultat du calcul</h1>
                    <p style="text-align: center;">Le coefficient de diffusion D_AB est : {D_AB:.6e} cm²/s</p>
                    <p style="text-align: center;">L'erreur relative par rapport à la valeur expérimentale est : {error:.2f} %</p>
                    <div style="text-align: center;">
                        <a href="/">Retour à l'accueil</a> | 
                        <a href="/page2">Retour au formulaire</a>
                    </div>
                </body>
            </html>
        """
    except ValueError:
        return """
            <html>
                <head>
                    <title>Erreur</title>
                </head>
                <body>
                    <h1 style="text-align: center;">Valeurs non valides. Veuillez entrer des nombres valides.</h1>
                    <div style="text-align: center;">
                        <a href="/page2">Retour au formulaire</a>
                    </div>
                </body>
            </html>
        """

# Gestion des erreurs pour les pages non existantes
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
