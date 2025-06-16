# 🧪 Guide de Test SmartOptimizer v1.1.0

## 🎯 Tests Recommandés par Niveau

### 🟢 **Niveau 1 : Tests Sécurisés (Aucun Risque)**

#### 1.1 Validation de l'Installation
```bash
# Test de la structure du projet
python3 tests/test_project_structure.py

# Vérification des permissions
ls -la src/analyzers/*.py src/optimizers/*.py
```

#### 1.2 Tests de Détection (Lecture Seule)
```bash
# Détection des services cloud (SANS modification)
python3 src/analyzers/cloud_services_detector.py ~/

# Vue d'ensemble rapide
python3 src/analyzers/ultra_quick_overview.py ~/Desktop

# Analyse des imbrications (mode lecture)
python3 src/analyzers/cloud_nesting_analyzer.py ~/
```

#### 1.3 Vérification de Sécurité
```bash
# Test de sécurité cloud
./scripts/quick_cloud_safety_check.sh

# Vérification plus complète
python3 src/utils/check_cloud_sync_status.py
```

---

### 🟡 **Niveau 2 : Tests avec Simulation (Mode Sécurisé)**

#### 2.1 Test d'Optimisation en Mode Simulation
```bash
# Créer un dossier de test
mkdir -p ~/SmartOptimizer_Test
cd ~/SmartOptimizer_Test
echo "Test file 1" > test1.txt
echo "Test file 1" > test1_copy.txt  # Doublon volontaire
echo "Different content" > test2.txt

# Tester l'optimiseur (MODE SIMULATION par défaut)
python3 ~/SmartOptimizer/src/optimizers/quick_smart_optimizer.py ~/SmartOptimizer_Test
```

#### 2.2 Test de Réorganisation en Simulation
```bash
# Créer une structure désorganisée
mkdir -p ~/SmartOptimizer_Test/random_files
echo "Document content" > ~/SmartOptimizer_Test/random_files/document.pdf
echo "Image data" > ~/SmartOptimizer_Test/random_files/photo.jpg

# Tester la réorganisation (MODE SIMULATION)
python3 ~/SmartOptimizer/src/reorganizers/smart_reorganizer.py ~/SmartOptimizer_Test
```

---

### 🔴 **Niveau 3 : Tests Réels (Précautions Requises)**

⚠️ **IMPORTANT** : Toujours créer des sauvegardes avant les tests réels

#### 3.1 Préparation Sécurisée
```bash
# 1. Vérifier la sécurité cloud OBLIGATOIRE
./scripts/quick_cloud_safety_check.sh
# → Attendre le FEU VERT avant de continuer

# 2. Créer une sauvegarde Time Machine
sudo tmutil startbackup

# 3. Créer un dossier de test réel
cp -r ~/Desktop/quelques_fichiers ~/SmartOptimizer_Real_Test
```

#### 3.2 Test Réel Contrôlé
```bash
# Modifier la configuration pour le mode réel
cd ~/SmartOptimizer
cp smartoptimizer.conf smartoptimizer.conf.backup

# Éditer temporairement pour un test
sed 's/SIMULATION_MODE=true/SIMULATION_MODE=false/' smartoptimizer.conf.backup > smartoptimizer.conf

# Test sur le dossier de test UNIQUEMENT
python3 src/optimizers/quick_smart_optimizer.py ~/SmartOptimizer_Real_Test

# Restaurer la configuration sécurisée
mv smartoptimizer.conf.backup smartoptimizer.conf
```

---

## 🔧 Tests Spécialisés Cloud

### ☁️ **Test de Détection Multi-Cloud**
```bash
# Si vous avez plusieurs services cloud, tester la détection
python3 src/analyzers/cloud_services_detector.py ~/

# Analyser les imbrications si services multiples détectés
python3 src/analyzers/cloud_nesting_analyzer.py ~/
```

### 🔄 **Test de Déduplication (Simulation)**
```bash
# Créer des doublons artificiels pour tester
mkdir -p ~/CloudTest/{Service1,Service2}
echo "Same content" > ~/CloudTest/Service1/file.txt
echo "Same content" > ~/CloudTest/Service2/file.txt

# Tester la déduplication (MODE SIMULATION)
python3 src/optimizers/cloud_deduplication_optimizer.py ~/CloudTest
```

---

## 🧪 Tests Avancés

### 🐳 **Test Docker (Isolation Complète)**
```bash
# Construire l'image Docker
cd docker
docker build -t smartoptimizer-test .

# Tester dans un conteneur isolé
docker run -v ~/SmartOptimizer_Test:/home/optimizer/data smartoptimizer-test overview
```

### 📊 **Test de Performance**
```bash
# Chronométrer l'analyse
time python3 src/analyzers/ultra_quick_overview.py ~/

# Test sur un gros répertoire
time python3 src/analyzers/cloud_services_detector.py ~/
```

---

## ✅ Validation des Résultats

### 📋 **Checklist de Validation**

#### Après chaque test, vérifier :
- [ ] **Aucun fichier supprimé** par accident
- [ ] **Sauvegardes créées** si mode réel utilisé
- [ ] **Logs d'erreur** dans le terminal
- [ ] **Espace disque** avant/après
- [ ] **Services cloud** toujours fonctionnels

#### En cas de problème :
```bash
# Vérifier les sauvegardes
ls -la ~/SmartOptimizer_Backups/

# Restaurer si nécessaire
cp -r ~/SmartOptimizer_Backups/latest/* ~/destination/

# Signaler le bug
echo "Problème détecté avec [description]" > ~/smartoptimizer_bug_report.txt
```

---

## 🎯 Scénarios de Test Spécifiques

### Scénario 1 : "J'ai iCloud + Google Drive"
```bash
# 1. Détecter les services
python3 src/analyzers/cloud_services_detector.py ~/

# 2. Analyser les imbrications
python3 src/analyzers/cloud_nesting_analyzer.py ~/

# 3. Vérifier la sécurité
./scripts/quick_cloud_safety_check.sh

# 4. Si sûr, workflow complet en simulation
./examples/cloud_optimization_workflow.sh
```

### Scénario 2 : "Mon Desktop est en désordre"
```bash
# 1. Analyser le Desktop
python3 src/analyzers/ultra_quick_overview.py ~/Desktop

# 2. Proposer une réorganisation (simulation)
python3 src/reorganizers/smart_reorganizer.py ~/Desktop

# 3. Si satisfait, appliquer (avec sauvegarde)
# → Modifier simulation_mode = false temporairement
```

### Scénario 3 : "Je suis développeur avec plein de projets"
```bash
# 1. Analyser les projets
python3 src/analyzers/comprehensive_analyzer.py ~/Projects

# 2. Workflow développeur complet
./examples/developer_cleanup.sh

# 3. Optimiser par technologie
python3 src/reorganizers/smart_reorganizer.py ~/Projects
```

---

## 🚨 Protocole d'Urgence

### En cas de problème :
1. **ARRÊT IMMÉDIAT** : Ctrl+C
2. **Vérifier les sauvegardes** : `ls ~/SmartOptimizer_Backups/`
3. **Restaurer si nécessaire** : `cp -r backup/* destination/`
4. **Signaler le bug** avec les détails
5. **Revenir en mode simulation** : `SIMULATION_MODE=true`

---

## 📞 Support et Débogage

### Obtenir de l'aide :
```bash
# Logs détaillés
python3 -v src/analyzers/cloud_services_detector.py ~/

# Version et configuration
cat README.md | grep version
cat smartoptimizer.conf

# État du système
df -h  # Espace disque
ps aux | grep -E "(cloud|sync|drive)"  # Processus cloud
```

### Contacter le support :
- 📖 **Documentation** : `cat docs/user-guide.md`
- 🐛 **Bugs** : GitHub Issues avec logs
- 💬 **Questions** : GitHub Discussions
- 📧 **Urgent** : contact@smartoptimizer.dev

---

## 🏆 Tests de Validation Finale

### Avant de déclarer "ça marche" :
1. ✅ **Tests niveau 1** passés sans erreur
2. ✅ **Tests niveau 2** avec résultats attendus  
3. ✅ **Sauvegarde** Time Machine récente
4. ✅ **Sécurité cloud** validée
5. ✅ **Un test réel** sur dossier non-critique réussi

### Commencer par :
```bash
# Test le plus simple et sûr
python3 tests/test_project_structure.py
python3 src/analyzers/cloud_services_detector.py ~/
```

**Bon testing ! 🚀**