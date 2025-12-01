from classes import Fragata, Corbeta, Submarino, Flota, Capitan, SistemaArmas, SistemaSensores


def main():
    # Crear plataformas con sus sistemas (composición automática si no se pasan)
    frag = Fragata("F-101", "España", 140.5, 4500, 28.0, misilesAntiaereos=6, helicopterosEmb=1, rolPrincipal='AA')
    cor = Corbeta("C-201", "Chile", 85.0, 1500, 25.0, misilesAntibuque=4, autonomiaDias=15)
    sub = Submarino("S-301", "Brasil", 70.0, 2200, 20.0, profundidadMaxima=400, tipoPropulsion='nuclear', tubosLanzatorpedos=6)

    # Crear capitán y asumir mando
    cap_f = Capitan("Luis García", "Comandante", 15)
    cap_f.asumirMando(frag)

    cap_s = Capitan("María Pérez", "Capitán de Fragata", 12)
    cap_s.asumirMando(cor)

    # Corbeta sin capitán por ahora

    # Crear flota y agregar plataformas (agregación)
    flota = Flota("Atlántica", "Atlántico Norte")
    flota.agregarPlataforma(frag)
    flota.agregarPlataforma(cor)
    flota.agregarPlataforma(sub)

    # Demostración de acciones
    frag.navegar(90, 20)
    frag.sistema_sensores.escanearSuperficie()
    frag.dispararMisilAA()

    cor.realizarPatrulla(costera=True)
    cor.dispararMisilAntibuque()

    sub.sumergirse(200)
    sub.lanzarTorpedo()
    sub.emerger()

    # Ordenar ataque desde la flota (se envía orden a las plataformas con capitán)
    flota.ordenarAtaque()

    # Recibir daño y comprobar operatividad (si se destruye, sus sistemas son parte de la plataforma)
    frag.recibirDanio(120)
    frag.estaOperativa()


if __name__ == '__main__':
    main()
