# Prompt d'extraction — Terre d'Arran (MJ Obsidian Vault)

## Contexte

Tu analyses des livres de règles du jeu de rôle **Terre d'Arran** (TdA). Ton rôle est d'extraire toutes les informations pertinentes et de les structurer en fichiers Markdown individuels prêts pour un vault Obsidian de Maître du Jeu (MJ).

Le jeu se déroule dans un univers de fantasy médiévale, sur le continent d'**Arran**. Les personnages joueurs incarnent des aventuriers issus de **profils** variés (guerrier, mage, rôdeur…). Ils évoluent dans un monde riche en royaumes, factions politiques, créatures dangereuses, magie et objets légendaires.

---

## Instructions générales

- Extrais **chaque entité distincte** (règle, profil, compétence, lieu, PNJ, sort, créature...) dans un bloc séparé.
- Utilise le marqueur `<!-- ENTITY: Catégorie/Sous-catégorie/Nom -->` avant chaque entité.
- Rédige en **français** (le jeu est en français).
- Inclus toujours le **frontmatter YAML** Obsidian avec les métadonnées.
- Utilise les **liens Obsidian** `[[Nom]]` pour référencer d'autres entités.
- Préfixe les tags avec `#` : `#pnj`, `#lieu`, `#sort`, `#règle`, `#créature`, etc.
- Si une information est **incertaine** ou **implicite**, marque-la avec `> *Déduction:*` ou `> *Incertain:*`.
- Ne fabrique pas d'information absente du texte.

---

## Catégories à extraire et format attendu

---

### 1. PROFILS DE PERSONNAGE (`Regles/Personnage/Profils/`)

Extrait chaque **Profil** (archétype de personnage joueur : guerrier, mage, rôdeur, etc.).

**Marqueur:** `<!-- ENTITY: Regles/Personnage/Profils/NomDuProfil -->`

**Format:**
```markdown
---
tags: [#profil, #personnage-joueur, #règle]
source: "Nom du livre, p. XX"
---

# Profil : [Nom]

## Description
[Description narrative du profil et de sa place dans le monde d'Arran]

## Caractéristiques principales
[Caractéristiques ou attributs clés associés à ce profil]

## Compétences de profil
- [[CompétenceA]] — [brève description]
- [[CompétenceB]] — [brève description]

## Traits de profil
- [[Trait]] — [description]

## Équipement de départ
- [Item 1]
- [Item 2]

## Évolution
[Comment ce profil progresse, montée en niveau ou déblocage de capacités]

## Notes MJ
[Conseils pour mettre en scène ou exploiter ce type de personnage]
```

---

### 2. COMPÉTENCES (`Regles/Personnage/Competences/`)

Extrait chaque **Compétence** utilisée lors des jets de dés.

**Marqueur:** `<!-- ENTITY: Regles/Personnage/Competences/NomDeLaCompetence -->`

**Format:**
```markdown
---
tags: [#compétence, #règle]
caractéristique: "[Caractéristique associée]"
source: "Nom du livre, p. XX"
---

# Compétence : [Nom]

## Caractéristique associée
[[NomCaractéristique]]

## Description
[Ce que couvre cette compétence]

## Utilisation de base
[Procédure standard de jet]

## Réussites supplémentaires
| Succès | Effet |
|--------|-------|
| +1     | ...   |
| +2     | ...   |

## Situations typiques
- [Exemple 1]
- [Exemple 2]

## Interactions
- Lié à : [[AutreCompétence]], [[Trait]]
```

---

### 3. TRAITS (`Regles/Personnage/Traits/`)

Extrait chaque **Trait** (capacité passive ou active, don, défaut).

**Marqueur:** `<!-- ENTITY: Regles/Personnage/Traits/NomDuTrait -->`

**Format:**
```markdown
---
tags: [#trait, #règle]
profil: "[Profil associé ou 'Général']"
type: "[Passif/Actif/Défaut]"
source: "Nom du livre, p. XX"
---

# Trait : [Nom]

## Type
[Passif / Actif / Défaut]

## Effet
[Description complète de l'effet]

## Conditions d'activation *(si actif)*
[Ce qui déclenche ou permet l'utilisation]

## Interactions
- Synergies avec : [[AutreTrait]], [[Compétence]]

## Exemple d'utilisation
[Situation concrète de jeu]
```

---

### 4. MÉCANIQUE DU JEU (`Regles/Mecanique/`)

Extrait chaque **règle ou système** de jeu distinct.

**Marqueur:** `<!-- ENTITY: Regles/Mecanique/NomDeLaRegle -->`

Sujets typiques à extraire :
- Résolution des actions (jet de dés, seuils de réussite)
- Combat (initiative, attaque, défense, blessures)
- Repos et récupération
- Déplacements et voyages
- Moral et peur
- Commerce et ressources
- Progression et expérience

**Format:**
```markdown
---
tags: [#règle, #mécanique]
source: "Nom du livre, p. XX"
---

# [Nom de la règle]

## Résumé
[Une phrase : à quoi sert cette règle]

## Procédure
1. [Étape 1]
2. [Étape 2]
3. [Étape 3]

## Tableau de référence *(si applicable)*
| Situation | Modificateur |
|-----------|-------------|
| ...       | ...         |

## Exceptions et cas particuliers
- [Cas 1]
- [Cas 2]

## Interactions avec d'autres règles
- Lié à : [[AutreRegle]]

## Aide-mémoire MJ
[Ce que le MJ doit retenir en priorité]
```

---

### 5. VILLES ET CITÉS (`Lieux/Villes/`)

Extrait chaque **ville, cité ou village** nommé.

**Marqueur:** `<!-- ENTITY: Lieux/Villes/NomDeLaVille -->`

**Format:**
```markdown
---
tags: [#ville, #lieu]
région: "[[NomDeLaRégion]]"
population: "[Taille approximative ou catégorie]"
faction_dominante: "[[NomFaction]]"
source: "Nom du livre, p. XX"
---

# Lieu : [Nom]

## Description
[Ambiance, architecture, situation géographique]

## Points d'intérêt
- [Lieu 1] — [description courte]
- [Lieu 2] — [description courte]

## Personnages notables
- [[PNJ1]] — [rôle]
- [[PNJ2]] — [rôle]

## Factions présentes
- [[Faction]] — [influence]

## Rumeurs et informations
[Ce que les joueurs peuvent apprendre ici]

## Secrets
> *Secret MJ:* [Information cachée]

## Scènes possibles
- [Scène ou événement qui peut se produire ici]
```

---

### 6. DONJONS ET SITES (`Lieux/Donjons/`)

Extrait chaque **donjon, ruine, crypte ou site d'aventure** nommé.

**Marqueur:** `<!-- ENTITY: Lieux/Donjons/NomDuSite -->`

**Format:**
```markdown
---
tags: [#donjon, #lieu, #aventure]
région: "[[NomDeLaRégion]]"
dangerosité: [1-5]
source: "Nom du livre, p. XX"
---

# Site : [Nom]

## Histoire
[Origine et histoire du lieu]

## Description générale
[Ambiance, état de conservation, dangers notables]

## Factions ou habitants
- [[Créature ou groupe]] — [présence]

## Trésors et récompenses potentiels
- [[Objet ou artefact]]

## Pièges et dangers
- [Danger 1]

## Secrets
> *Secret MJ:* [Révélation cachée]

## Hooks d'aventure
- [Raison pour que les PJ s'y rendent]
```

---

### 7. RÉGIONS (`Lieux/Regions/`)

Extrait chaque **région, royaume ou territoire** nommé.

**Marqueur:** `<!-- ENTITY: Lieux/Regions/NomDeLaRegion -->`

**Format:**
```markdown
---
tags: [#région, #lieu, #géographie]
type: "[Royaume/Forêt/Désert/Montagne/Marais/Autre]"
source: "Nom du livre, p. XX"
---

# Région : [Nom]

## Description géographique
[Terrains, climat, caractéristiques naturelles]

## Histoire et politique
[Qui dirige, conflits actuels, histoire récente]

## Villes principales
- [[Ville1]]
- [[Ville2]]

## Dangers et créatures
- [[Créature]] — [zone de présence]

## Ressources
[Ce que cette région produit ou possède]

## Factions actives
- [[Faction]] — [rôle dans la région]

## Points d'intérêt notables
- [[Donjon ou site]]
```

---

### 8. FACTIONS (`Factions/`)

Extrait chaque **faction, guilde, ordre ou organisation** nommée.

**Marqueur:** `<!-- ENTITY: Factions/NomDeLaFaction -->`

**Format:**
```markdown
---
tags: [#faction, #organisation]
type: "[Guilde/Ordre/Culte/Royaume/Bande/Autre]"
puissance: [1-5]
source: "Nom du livre, p. XX"
---

# Faction : [Nom]

## Idéologie et objectifs
[Ce en quoi ils croient, ce qu'ils veulent accomplir]

## Structure
[Hiérarchie interne, comment on y entre]

## Chef
[[NomDuChef]]

## Membres notables
- [[PNJ1]] — [rôle]
- [[PNJ2]] — [rôle]

## Territoires et ressources
- [[Lieu ou ressource contrôlée]]

## Alliés et ennemis
- Alliés : [[AutreFaction]]
- Ennemis : [[AutreFaction]]

## Tensions et conflits actuels
[Problèmes internes ou externes en cours]

## Comment les impliquer en jeu
[Hooks et conseils MJ]
```

---

### 9. PNJ (`PNJ/`)

Extrait chaque **personnage non-joueur** nommé avec suffisamment de détails.

**Marqueur:** `<!-- ENTITY: PNJ/NomDuPNJ -->`

**Format:**
```markdown
---
tags: [#pnj]
faction: "[[NomFaction]]"
rôle: "[Profession ou rôle social]"
localisation: "[[NomDuLieu]]"
statut: "[Vivant/Mort/Inconnu]"
source: "Nom du livre, p. XX"
---

# PNJ : [Nom]

## Description physique
[Apparence, signes distinctifs]

## Personnalité
[En 2-3 adjectifs et une phrase]

## Motivation
[Ce que ce PNJ veut avant tout]

## Liens
- Allié de : [[AutrePNJ]]
- Ennemi de : [[AutrePNJ]]
- Membre de : [[Faction]]

## Caractéristiques *(si précisées)*
| Caract. | Valeur |
|---------|--------|
| ...     | X      |

## Compétences notables
- [[Compétence]] X

## Traits
- [[Trait]]

## Secrets
> *Secret MJ:* [Ce que les joueurs ne savent pas]

## Scènes et interactions
- [Comment ce PNJ peut intervenir en jeu]
```

---

### 10. BESTIAIRE (`Bestiaire/`)

Extrait chaque **créature ou monstre** décrit dans les règles.

**Marqueur:** `<!-- ENTITY: Bestiaire/NomDeLaCreature -->`

**Format:**
```markdown
---
tags: [#créature, #bestiaire]
type: "[Humanoïde/Animal/Mort-vivant/Démon/Fée/Autre]"
dangerosité: [1-5]
habitat: "[Forêt/Montagne/Donjon/Partout/...]"
source: "Nom du livre, p. XX"
---

# Créature : [Nom]

## Description
[Apparence, comportement, habitat naturel]

## Caractéristiques
| Caract.  | Valeur |
|----------|--------|
| ...      | X      |
| PV       | X      |
| Armure   | X      |

## Attaques
| Attaque | Dégâts | Effet spécial |
|---------|--------|---------------|
| ...     | XdX    | ...           |

## Capacités spéciales
- [Capacité 1] : [description]

## Tactiques
[Comment cette créature se comporte en combat ou en chasse]

## Loot
[Ce qu'on peut obtenir en la vainquant]

## Régions associées
- [[NomRégion]]

## Rumeurs et légendes
[Ce que les habitants en disent]
```

---

### 11. ÉQUIPEMENT — Armes (`Equipement/Armes/`)

**Marqueur:** `<!-- ENTITY: Equipement/Armes/NomDeLArme -->`

**Format:**
```markdown
---
tags: [#arme, #équipement]
type: "[Corps-à-corps/Distance/Jet]"
dégâts: "[XdX]"
prix: "[Valeur en pièces]"
source: "Nom du livre, p. XX"
---

# Arme : [Nom]

## Caractéristiques
| Propriété    | Valeur |
|--------------|--------|
| Dégâts       | XdX    |
| Portée       | ...    |
| Encombrement | X      |
| Prix         | X po   |

## Propriétés spéciales
- [Propriété 1]

## Description
[Apparence, matériaux, usage]

## Notes MJ
[Cas particuliers, usages créatifs]
```

---

### 12. ÉQUIPEMENT — Armures (`Equipement/Armures/`)

**Marqueur:** `<!-- ENTITY: Equipement/Armures/NomDeLArmure -->`

**Format:**
```markdown
---
tags: [#armure, #équipement]
protection: [Valeur numérique]
prix: "[Valeur en pièces]"
source: "Nom du livre, p. XX"
---

# Armure : [Nom]

## Caractéristiques
| Propriété      | Valeur |
|----------------|--------|
| Protection     | X      |
| Encombrement   | X      |
| Prix           | X po   |

## Propriétés spéciales
- [Propriété 1]

## Description
[Apparence, matériaux, type]
```

---

### 13. ÉQUIPEMENT — Objets divers (`Equipement/Objets/`)

**Marqueur:** `<!-- ENTITY: Equipement/Objets/NomDeLObjet -->`

**Format:**
```markdown
---
tags: [#objet, #équipement]
prix: "[Valeur en pièces]"
source: "Nom du livre, p. XX"
---

# Objet : [Nom]

## Effet
[Ce que fait cet objet mécaniquement]

## Description
[Apparence et usage concret]

## Prix
[Valeur estimée]
```

---

### 14. MAGIE — Sorts (`Magie/Sorts/`)

**Marqueur:** `<!-- ENTITY: Magie/Sorts/NomDuSort -->`

**Format:**
```markdown
---
tags: [#sort, #magie]
domaine: "[[NomDuDomaine]]"
niveau: [1-X]
coût: "[Coût en mana/points/autre]"
source: "Nom du livre, p. XX"
---

# Sort : [Nom]

## Domaine
[[NomDuDomaine]]

## Niveau
[Niveau du sort]

## Coût
[Ressource dépensée pour lancer]

## Portée
[Soi-même / Contact / X mètres / Zone]

## Durée
[Instantané / X rounds / X minutes / Permanent]

## Effet
[Description complète de l'effet]

## Réussites supplémentaires *(si applicable)*
| Succès | Effet |
|--------|-------|
| +1     | ...   |

## Effets de surcharge ou d'échec critique
[Ce qui se passe en cas d'échec grave]

## Notes MJ
[Usages tactiques, interactions notables]
```

---

### 15. MAGIE — Rituels (`Magie/Rituels/`)

**Marqueur:** `<!-- ENTITY: Magie/Rituels/NomDuRituel -->`

**Format:**
```markdown
---
tags: [#rituel, #magie]
domaine: "[[NomDuDomaine]]"
durée_préparation: "[X minutes/heures/jours]"
source: "Nom du livre, p. XX"
---

# Rituel : [Nom]

## Domaine
[[NomDuDomaine]]

## Composantes
- [Ingrédient ou condition 1]
- [Ingrédient ou condition 2]

## Durée de préparation
[Temps requis]

## Effet
[Description complète]

## Conditions d'échec
[Ce qui peut mal tourner]

## Notes MJ
[Comment l'utiliser en scénario]
```

---

### 16. MAGIE — Domaines (`Magie/Domaines/`)

Extrait chaque **école ou domaine de magie** décrit dans les règles.

**Marqueur:** `<!-- ENTITY: Magie/Domaines/NomDuDomaine -->`

**Format:**
```markdown
---
tags: [#domaine, #magie, #règle]
source: "Nom du livre, p. XX"
---

# Domaine : [Nom]

## Thématique
[Ce que représente ce domaine — feu, nature, mort, illusion…]

## Accès
[Qui peut apprendre ce domaine, conditions]

## Sorts associés
- [[Sort1]]
- [[Sort2]]

## Rituels associés
- [[Rituel1]]

## Notes MJ
[Comment intégrer ce domaine en jeu, PNJ qui l'utilisent]
```

---

### 17. TABLES ALÉATOIRES (`Tables/`)

Extrait chaque **table aléatoire** utilisable en jeu.

**Marqueur:** `<!-- ENTITY: Tables/NomDeLaTable -->`

**Format:**
```markdown
---
tags: [#table, #outil-mj]
type: "[Rencontre/Loot/Météo/Événement/Rumeur/Autre]"
dé: "[d6/d8/d10/d12/d20/d66/Autre]"
source: "Nom du livre, p. XX"
---

# Table : [Nom]

## Usage
[Dans quelle situation utiliser cette table]

## Table

| Résultat | Contenu |
|----------|---------|
| 1        | ...     |
| 2        | ...     |
| ...      | ...     |

## Notes MJ
[Conseils d'utilisation, modifications suggérées]
```

---

## Règles de déduplication

Si une entité apparaît dans plusieurs livres :
1. **Crée un seul fichier** par entité unique
2. Ajoute une section `## Sources` listant tous les livres
3. Signale les **contradictions** entre livres avec `> ⚠️ Contradiction:`
4. Garde la version la plus complète / récente comme référence

---

## Format des INDEX par dossier

Pour chaque dossier, génère un `INDEX.md` :

**Marqueur:** `<!-- ENTITY: INDEX/CheminDuDossier -->`

```markdown
---
tags: [#index]
---

# Index : [Nom du dossier]

## Contenu
| Nom | Description courte | Tags |
|-----|-------------------|------|
| [[Fichier1]] | ... | #tag |
| [[Fichier2]] | ... | #tag |

## Sous-dossiers
- [[SousDossier/INDEX]]

## Liens rapides MJ
- [Lien vers entité souvent utilisée]
```

---

## Ce qu'il faut NE PAS extraire

- Le texte narratif de fiction (nouvelles, exemples de jeu immersifs)
- Les crédits et mentions légales
- La table des matières (elle sera reconstruite via les INDEX)
- Les répétitions exactes d'une règle déjà extraite

---

## Priorité d'extraction (du plus au moins important)

1. **Règles de base** — compétences, traits, profils, mécanique
2. **Sorts et rituels** — avec coût et effets mécaniques complets
3. **PNJ avec nom propre** — toujours un fichier dédié
4. **Créatures du bestiaire** — avec stats et tactiques
5. **Lieux nommés** — villes, donjons, régions
6. **Factions et organisations** — avec motivations
7. **Équipement** — armes, armures, objets notables
8. **Tables aléatoires** — synthétisées en tableaux Markdown

---

*Ce prompt est conçu pour être utilisé avec un MCP server qui découpe les PDFs en chunks de 10-15k caractères et les soumet un par un à l'IA pour extraction.*
