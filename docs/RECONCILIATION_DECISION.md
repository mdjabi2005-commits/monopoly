# Décision d'Architecture : Réconciliation Bornée API vs Relevés PDF

> **Projet** : Gestio & Monopoly  
> **Date de décision** : 19 août 2026  
> **Statut** : Validé  

---

## 1. Contexte et Problématique

Gestio combine deux sources de données bancaires :
1. **L'API bancaire (Enable Banking)** : Flux temps réel / 90 jours glissants. Les transactions sont découpées en champs ISO structurés (`creditor_name`, `booking_date`, `remittance_information`).
2. **Les Relevés PDF mensuels (Monopoly)** : Vérité légale et historique complet depuis l'ouverture des comptes. Les transactions sont imprimées sous forme de lignes compactées (ex: `19/06 ACHAT CB LECLERC CAISSE 18.06.26 CARTE NUMERO 486`).

### Le Constat
Les libellés textuels ne correspondent pas mot à mot entre l'API et le PDF. Cependant, **la réconciliation n'a pas besoin de faire de la recherche probabiliste à grande échelle**, car elle s'exécute sur une **fenêtre temporelle courte et bornée**.

---

## 2. Le Principe de la Fenêtre Mensuelle Biparti (~30 transactions)

Dans le cycle de vie du produit, une personne effectue en moyenne **30 à 50 transactions par mois et par compte**.

```
    [Passé lointain : > 90 jours]            [Mois M écoulé]              [Temps réel : Aujourd'hui]
◄──────────────────────────────────────┼─────────────────────────────┼────────────────────────────────►
          100% PDF Historique                     FUSION                     100% API Enable Banking
          (Aucun conflit API)                 API ⚡ vs PDF 📄               (En attente du relevé le 8)
                                            (~30 transactions)
```

1. **Passé lointain (> 90 jours)** : Importé à 100% par Monopoly depuis les relevés PDF historiques. Aucun risque de collision API.
2. **Temps réel en cours** : Fourni par l'API Enable Banking au jour le jour.
3. **Le 8 de chaque mois (Bilan mensuel)** : Lors de la parution du relevé officiel, Gestio fusionne le mois écoulé. Le sous-ensemble à réconcilier ne contient que **~30 transactions**.

---

## 3. Algorithme de Réconciliation en 3 Niveaux

Sur un sous-ensemble borné à 30 transactions, l'association est quasiment déterministe :

### Niveau 1 : Le Filtre Mathématique (Compte + Montant exact au centime + Date)
- `accountId_API == accountId_PDF`
- `amountCents_API == amountCents_PDF` (exactitude absolue au centime près)
- `|date_API - date_PDF| <= 1 jour` (tolérance pour la date de compensation bancaire)

### Niveau 2 : Résolution des Collisions (Ordre FIFO + Tokens)
Pour le cas rare où deux montants identiques se produisent le même jour (ex: deux achats à 2,50 €) :
- **Règle FIFO** : La première transaction du relevé s'associe à la première transaction de l'API.
- **Score Jaccard sur tokens normalisés** : Validation par les mots-clés communs du commerçant (`LECLERC`, `SNCF`, `UBER`).

### Niveau 3 : Clé Primaire Native pour les Fintechs & Virements
- Lorsque le relevé ou l'API fournit une référence unique (`Réf. externe`, `UUID`, `Order ID`, référence virement) :
- La réconciliation et l'anti-doublon sont immédiats en $O(1)$ par égalité stricte de la référence.

---

## 4. Détection et Réconciliation des Virements Internes

$$\text{Virement Interne} \iff (\text{IBAN Source} \in \text{Mes Comptes Gestio}) \land (\text{IBAN Cible} \in \text{Mes Comptes Gestio})$$

- Les IBANs mentionnés dans les libellés (ex: Trade Republic `FR76... à DE43...`) sont extraits et conservés.
- Si les deux comptes appartiennent à l'utilisateur, l'opération est qualifiée de `virement_intercompte` :
  - La sortie $(-X\text{ €})$ et l'entrée $(+X\text{ €})$ sont liées.
  - **Neutralité financière** : Le virement n'est pas compté comme une dépense ou un revenu externe, préservant la justesse de la trésorerie disponible.

---

## 5. Preuves Empiriques

Cette décision repose sur les validations réelles obtenues sur le corpus bancaire complet :
- **Nickel** (11 fichiers, 84 transactions) : 100% validé.
- **La Banque Postale** (13 fichiers, 361 transactions) : 100% validé.
- **Trade Republic** (2 fichiers, 274 transactions) : 100% validé avec extraction des doubles IBANs.
- **Sumeria** (1 fichier, 8 transactions) : 100% validé avec extraction des UUIDs externes.
