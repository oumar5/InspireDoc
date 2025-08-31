#!/bin/bash

# Script de développement Docker pour InspireDoc
# Usage: ./docker-dev.sh [command]

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier que Docker est installé
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
}

# Vérifier le fichier .env
check_env() {
    if [ ! -f ".env" ]; then
        log_warning "Fichier .env non trouvé. Création depuis .env.example..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            log_info "Fichier .env créé. Veuillez le configurer avec vos clés API."
        else
            log_error "Fichier .env.example non trouvé."
            exit 1
        fi
    fi
}

# Construire l'image de développement
build_dev() {
    log_info "Construction de l'image de développement..."
    docker-compose -f docker-compose.dev.yml build
    log_success "Image de développement construite avec succès!"
}

# Démarrer en mode développement
start_dev() {
    log_info "Démarrage d'InspireDoc en mode développement..."
    docker-compose -f docker-compose.dev.yml up -d
    
    # Attendre que le service soit prêt
    log_info "Attente du démarrage du service..."
    sleep 5
    
    # Afficher les logs
    log_success "InspireDoc démarré en mode développement!"
    log_info "Application accessible sur: http://localhost:8501"
    log_info "Hot reload activé - les modifications du code seront automatiquement prises en compte."
    
    # Suivre les logs
    docker-compose -f docker-compose.dev.yml logs -f inspiredoc-dev
}

# Arrêter les services
stop_dev() {
    log_info "Arrêt des services de développement..."
    docker-compose -f docker-compose.dev.yml down
    log_success "Services arrêtés."
}

# Redémarrer les services
restart_dev() {
    log_info "Redémarrage des services..."
    stop_dev
    start_dev
}

# Afficher les logs
logs_dev() {
    docker-compose -f docker-compose.dev.yml logs -f
}

# Exécuter une commande dans le conteneur
exec_dev() {
    if [ $# -eq 0 ]; then
        log_info "Ouverture d'un shell dans le conteneur..."
        docker-compose -f docker-compose.dev.yml exec inspiredoc-dev /bin/bash
    else
        log_info "Exécution de la commande: $*"
        docker-compose -f docker-compose.dev.yml exec inspiredoc-dev "$@"
    fi
}

# Nettoyer les ressources Docker
clean() {
    log_info "Nettoyage des ressources Docker..."
    docker-compose -f docker-compose.dev.yml down -v --remove-orphans
    docker system prune -f
    log_success "Nettoyage terminé."
}

# Afficher l'aide
show_help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commandes disponibles:"
    echo "  build     - Construire l'image de développement"
    echo "  start     - Démarrer en mode développement avec hot reload"
    echo "  stop      - Arrêter les services"
    echo "  restart   - Redémarrer les services"
    echo "  logs      - Afficher les logs"
    echo "  shell     - Ouvrir un shell dans le conteneur"
    echo "  exec      - Exécuter une commande dans le conteneur"
    echo "  clean     - Nettoyer les ressources Docker"
    echo "  help      - Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 start                    # Démarrer en mode développement"
    echo "  $0 exec pip install package # Installer un package"
    echo "  $0 shell                   # Ouvrir un shell interactif"
}

# Fonction principale
main() {
    check_docker
    check_env
    
    case "${1:-start}" in
        build)
            build_dev
            ;;
        start)
            build_dev
            start_dev
            ;;
        stop)
            stop_dev
            ;;
        restart)
            restart_dev
            ;;
        logs)
            logs_dev
            ;;
        shell)
            exec_dev
            ;;
        exec)
            shift
            exec_dev "$@"
            ;;
        clean)
            clean
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Commande inconnue: $1"
            show_help
            exit 1
            ;;
    esac
}

# Exécuter la fonction principale avec tous les arguments
main "$@"