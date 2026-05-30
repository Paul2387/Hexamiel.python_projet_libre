document.addEventListener("DOMContentLoaded", function(){

    console.log("JS chargé");
    const form = document.querySelector("form");
    if (!form) return;
    const champNom = document.querySelector("input[name='Nom']");

    const champMdp = document.querySelector("input[name='mdp']");

     const champConfirm_Mdp = document.querySelector("input[name='confirme_mdp']");


     // Validation
     function ValiderChamp(champ, condition, message) {

        let erreur = champ.parentElement.querySelector(".message-erreur");
        if(!condition) {
            if(!errreur) {
                erreur = document.createElement("p");
                erreur.classList.add("message-erreur");
                champ.parentElement.appendChild(erreur);

            }
            erreur.textContext = message;
            champ.classlist.add("champ-invalide");
            return false;

        } else {
            if (erreur) erreur.remove();
            champ.classList.remove("champ-invalide");
            return true;

        }

        // Temps reel
        champNom.addEventListener("input", function() {
            validerChamp(
                champNom,
                champNom.value.trim().length >= 4,
                "Le nom doit contenir au moins 4 caractères");
            
        });

        champMdp.addEventListener("input", function() {
            validerChamp(
                champMdp,
                champMdp.value.trim().length >= 5,
                "Le Mot de passe doit contenir au moins 5 caractères");

            });

        champConfirm_Mdp.addEventListener("input", function() {
            validerChamp(
                champConfirm_Mdp,
                champConfirm_Mdp.value == champMdp.value,
                "Les mots de passe ne cprrespondent pas");

            });

        
        //submit
        form.addEventListener("submit", function(evenement){

            const Nom_ok = validerChamp(
                champNom,
                champNom.value.trim().length >= 4,
                "Le nom doit contenir au moins 4 caractères");

            
            const Mdp_ok = validerChamp(
                champMdp,
                champMdp.value.trim().length >= 5,
                "Le Mot de passe doit contenir au moins 5 caractères");

             const Confirm_mdp_ok = validerChamp(
                champMdp,
                champConfirm_Mdp.value == champMdp.value,
                "Les mots de passe de correspondent pas");

            if (!Nom_ok || !Mdp_ok || !Confirm_Mdp_ok) {
                evenement.preventDefault();
                return;
            }
                   

        });
            
    



     }
})
