import sys

# Funzione helper per stampare separatori e rendere il log leggibile
def log_sep(char='-', length=50):
    print(char * length)

def find_insertion_positions(genome, insertion_points):
    print(f"Cerco {insertion_points} in {genome}")
    position = []
    length = len(insertion_points)
    start = 0
    while True:
        pos = genome.find(insertion_points, start)
        if pos == -1:
            # print(f"Nessuna (altra) occorrenza trovata.")
            break
        point_found = pos + length
        print(f"Trovato match a indice {pos}, punto inserimento: {point_found}")
        position.append(point_found)
        start = pos + 1
    return position

def analizza_edit(genome, point, insertion, candidate_edit):
    # Pulizia input
    cand_clean = candidate_edit.replace(" ", "")

    # Troviamo tutte le posizioni di inserimento possibili per questo specifico point
    positions = find_insertion_positions(genome, point)

    # Se non troviamo il point nel genoma, ritorniamo errore massimo
    if not positions:
        return False, -1, len(insertion)

    default_idx = positions[0]

    # ------------------------------------------------------------------
    # 1. IL GENOMA È RIMASTO INVARIATO? (Edit Vuoto)
    # ------------------------------------------------------------------
    if cand_clean == genome:
        print(f"CASO 1: Genoma invariato per point {point}")
        if insertion in genome:
            return True, default_idx, 0
        else:
            return False, default_idx, len(insertion)

    # ------------------------------------------------------------------
    # 2. INSERZIONE GIÀ PRESENTE MA GENOMA MODIFICATO
    # ------------------------------------------------------------------
    if insertion in genome:
        print(f"CASO 2: Inserzione {insertion} già presente, ma genoma modificato (Errore)")
        return False, default_idx, len(insertion)

    # ------------------------------------------------------------------
    # 3. ANALISI STANDARD (Con controllo Prefisso + Suffisso)
    # ------------------------------------------------------------------
    # Inizializziamo a None per sapere se abbiamo trovato un match valido
    miglior_risultato = None

    for taglio in positions:
        fine_ins_edit = taglio + len(insertion)

        # A. Verifica Lunghezza
        if len(cand_clean) != len(genome) + len(insertion):
            continue

        # B. Controllo prefisso e suffisso
        prefisso_ok = cand_clean[:taglio] == genome[:taglio]
        suffisso_ok = cand_clean[fine_ins_edit:] == genome[taglio:]

        if prefisso_ok and suffisso_ok:
            part_inserita = cand_clean[taglio : fine_ins_edit]

            # Conta errori carattere per carattere
            conteggio = 0
            for i in range(len(insertion)):
                if part_inserita[i] != insertion[i]:
                    conteggio += 1
            curr_errori = conteggio

            # Aggiorna solo se è il miglior match trovato finora
            if miglior_risultato is None or curr_errori < miglior_risultato[2]:
                print(f"Check taglio {taglio}: Trovati {curr_errori} errori con {part_inserita}")
                miglior_risultato = (curr_errori == 0, taglio, curr_errori)

                if curr_errori == 0:
                    break

    # ------------------------------------------------------------------
    # 4. SE NESSUN MATCH STRUTTURALE È STATO TROVATO, RITORNA ERRORE MASSIMO
    # ------------------------------------------------------------------
    #IN QUESTO CASO POTRESTI ANCHE NON RITORNARE NULLA, MA PER COMPLETEZZA RITORNIAMO UN VALORE E NELLA FUNZIONE CHIAMANTE PRENDIAMO QUELLO CON MENO ERRORI (BEST MATCH)
    if miglior_risultato is None:
        # Nessun taglio valido trovato per questo point -> questo point NON spiega l'edit
        print(f"Nessun match strutturale trovato per point {point}")
        return False, -1, len(insertion) + 1  # +1 per penalizzare rispetto a match reali

    return miglior_risultato


def valuta_singolo_edit(edit, genome, k_points, k_insertions):
    """
    Analizza un singolo edit contro tutte le coppie Point/Insertion.
    Restituisce la lista di ipotesi ordinata per quel singolo edit.
    """
    risultati = []

    for p, ins in zip(k_points, k_insertions):
        is_corr, idx, err = analizza_edit(genome, p, ins, edit)
        risultati.append({
            'edit_originale': edit,
            'point': p,
            'insertion': ins,
            'errors': err
        })

    # Ordina le ipotesi per questo edit (la migliore in cima)
    risultati.sort(key=lambda x: x['errors'])
    return risultati


def analizza_tutti_edits(lista_edits, genome, k_points, k_insertions):
    """
    FUNZIONE PRINCIPALE RICHIESTA:
    Prende la LISTA di edits, cicla su di essi internamente,
    trova il best match per ognuno e restituisce la classifica globale finale.
    """
    log_sep('=')
    print(f"INIZIO ANALISI LISTA ({len(lista_edits)} edits)")

    output_globale = []

    for i, edit in enumerate(lista_edits):
        log_sep('-')
        print(f"Processing Edit #{i+1}: '{edit}'")

        # 1. Trova tutte le spiegazioni possibili per questo edit
        classifica_locale = valuta_singolo_edit(edit, genome, k_points, k_insertions)

        # 2. Prendi la migliore (vincitore locale)
        best_match = classifica_locale[0]
        print(f"Best match locale: Ins '{best_match['insertion']}' su '{best_match['point']}' con {best_match['errors']} errori")

        # 3. Aggiungilo alla lista globale
        output_globale.append(best_match)

    # 4. Ordina la lista globale (chi ha fatto meno errori in assoluto va sopra)
    output_globale.sort(key=lambda x: x['errors'])
    return output_globale

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    genome = "ACCGTGACCTGATGA"
    insertion_points = ["CC", "GA"]
    insertions = ["TTG", "CAA"]

    edits = [
        "ACCGTGACC TTG TGATGA",
        "ACC TGG GTGACCTGATGA",
        "ACCGTGACCTGATGA",
        "ACCGTGA AAG CCTGATGA",
        "ACCGTGA AAA CCTGATGA"
    ]

    # ORA CHIAMIAMO UNA SOLA FUNZIONE PASSANDO TUTTA LA LISTA
    risultati_finali = analizza_tutti_edits(edits, genome, insertion_points, insertions)

    print("\n" + "="*60)
    print("OUTPUT GENERATO:")
    for item in risultati_finali:
        print(f"\"{item['edit_originale']}\", # errori: {item['errors']} su insertion point {item['point']}")