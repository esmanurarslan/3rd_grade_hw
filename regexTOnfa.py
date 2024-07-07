import re
from graphviz import Digraph
import pandas as pd
def regex_al():
    print("NOT=  * ifadesi kendinden önce gelen değerin 0 dan sonsuza kadar tekrar edebileceğini,\n  + ifadesi kendinden önce gelen değerin en az bir kere dönmesi gerektiğini belirtirken,\n | ifadesi ise OR anlamında kullanılır ve yalnızca parantez içi ifadelerde kullanılır.\n")
    while True:
        regex = input("Lütfen içinde a, b, *, +, |, (, ) sembolleri bulunan bir regex ifadesi girin: ")
        if re.match("^[ab*+|()]+$", regex):
            return regex
        else:
            print("Geçersiz bir regex ifadesi girdiniz. Lütfen sadece a, b, *, +, |, (, ) sembollerini kullanın.")
            
def ifadeyi_listeye_ayır(ifade):
    liste = []
    i = 0
    while i < len(ifade):
        if ifade[i] == '(':
            parantez_ic = ''
            i += 1
            while ifade[i] != ')':
                parantez_ic += ifade[i]
                i += 1
            i += 1  # ')' karakterini atlayalım
            if i < len(ifade) and (ifade[i] == '*' or ifade[i] == '+'):
                liste.append(parantez_ic + ifade[i])  # Parantez içi + * veya +
                i += 1
            else:
                liste.append(parantez_ic)  # Sadece parantez içi
        else:
            sembol = ifade[i]
            i += 1
            if i < len(ifade) and (ifade[i] == '*' or ifade[i] == '+'):
                sembol += ifade[i]  # * veya + ekle
                i += 1
            liste.append(sembol)
    return liste

def baslangic_durumu_olustur():
    return "q0"

def gecis_olustur(durum, sembol, hedef_durum):
    return f"({durum}, {sembol}) -> {hedef_durum}"

def regex_gecisleri_olustur(liste, baslangic_durumu, hedef_durum):
    gecisler = []
    current_durum = baslangic_durumu
    for i in range(len(liste)):
        sembol = liste[i]
        if "+" in liste[i - 1]:
            yeni_durum = "q" + str(i + 3)
        else:
             yeni_durum = "q" + str(i + 1)

        if len(sembol) < 2:
            
            gecisler.append(gecis_olustur(current_durum, sembol, yeni_durum))
            current_durum = yeni_durum
        else:
            if sembol == 'a*' or sembol == 'b*':
                gecisler.append(gecis_olustur(current_durum, sembol[0], current_durum))

            elif sembol == 'a+' or sembol == 'b+':
                 yeni_durum = "q" + str(i + 1)
                 gecisler.append(gecis_olustur(current_durum, sembol[0], yeni_durum))
                 gecisler.append(gecis_olustur(yeni_durum, sembol[0], yeni_durum))
                 current_durum=yeni_durum
            
            elif sembol == 'ab*' or sembol == 'ba*':
                eski_durum="q"+str(i-1)
                yeni_durum = "q" + str(i + 1)
                if sembol[1]==liste[i-1]:
                    gecisler.append(gecis_olustur(current_durum, sembol[0], eski_durum))
                else:
                    gecisler.append(gecis_olustur(current_durum, sembol[0], yeni_durum))
                    gecisler.append(gecis_olustur(yeni_durum, sembol[1], current_durum))
            elif sembol == 'ab+' or sembol == 'ba+':
                yeni_durum = "q" + str(i + 1)
                yeni_durum2="q" + str(i + 2)
                yeni_durum3="q" + str(i + 3)
                gecisler.append(gecis_olustur(current_durum, sembol[0], yeni_durum))
                gecisler.append(gecis_olustur(yeni_durum, sembol[1], yeni_durum2))
                gecisler.append(gecis_olustur(yeni_durum2, sembol[0], yeni_durum3))
                gecisler.append(gecis_olustur(yeni_durum3, sembol[1], yeni_durum2))
                current_durum=yeni_durum2
            elif sembol == 'a|b' or sembol == 'b|a':
                yeni_durum = "q" + str(i + 1)
                gecisler.append(gecis_olustur(current_durum, sembol[0], yeni_durum))
                gecisler.append(gecis_olustur(current_durum, sembol[2], yeni_durum))
                current_durum = yeni_durum
            elif sembol == 'a|b*' or sembol == 'b|a*':
                yeni_durum = "q" + str(i + 1)
                gecisler.append(gecis_olustur(current_durum, sembol[0], current_durum))
                gecisler.append(gecis_olustur(current_durum, sembol[2], current_durum))
            elif sembol == 'a|b+' or sembol == 'b|a+':
                yeni_durum = "q" + str(i + 1)
                gecisler.append(gecis_olustur(current_durum, sembol[0], yeni_durum))
                gecisler.append(gecis_olustur(current_durum, sembol[2], yeni_durum))
                gecisler.append(gecis_olustur(yeni_durum, sembol[0], yeni_durum))
                gecisler.append(gecis_olustur(yeni_durum, sembol[2], yeni_durum))
                current_durum = yeni_durum        
            else:
                print("Geçersiz sembol:", sembol)
    
    if hedef_durum!='qh':
        gecisler.append(gecis_olustur(current_durum, '', hedef_durum))
    
    return gecisler

def draw_regex_graph(gecisler):
    dot = Digraph(comment='Regex Otomatonu')
    states = set()
    for gecis in gecisler:
        parts = gecis.split(' -> ')
        durum, sembol = parts[0][1:-1].split(', ')
        hedef_durum = parts[1]
        states.add(durum)
        states.add(hedef_durum)
        dot.edge(durum, hedef_durum, label=sembol)
    for state in states:
        if state == gecisler[-1].split(' -> ')[-1]:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)
    return dot

def optimize_transitions(transitions):
    optimized_transitions = []

    for transition in transitions:
        parts = transition.split(' -> ')
        if len(parts) != 2:
            print("Geçersiz geçiş ifadesi:", transition)
            continue

        source_symbol, target = parts
        source, symbol = source_symbol.strip('()').split(', ')

        # Hedef durumları ayırıp bir değerde toplayalım
        target_states_list = target.split(', ')
        target_states = ' '.join(target_states_list)

        found = False
        for i, optimized_transition in enumerate(optimized_transitions):
            if optimized_transition.startswith(f"({source}, {symbol})"):
                # Hedef durumu ekleyelim
                optimized_transitions[i] = f"({source}, {symbol}) -> {optimized_transition.split(' -> ')[1]}, {target_states}"
                found = True
                break   
        if not found:
            # Hedef durumu ekleyelim
            optimized_transitions.append(f"({source}, {symbol}) -> {target_states}")

    # Tüm hedef durumlarını bir tane süslü parantez içine alalım
    for i, optimized_transition in enumerate(optimized_transitions):
        parts = optimized_transition.split(' -> ')
        source_symbol = parts[0]
        target_states = parts[1] 
        optimized_transitions[i] = f"Geçiş: {source_symbol} -> {target_states}"

    return optimized_transitions

def tabloOlustur(girdi):
    nfa = {}
    aNfa={}
    for item in girdi:
        item = item.replace('(', '').replace('Geçiş: ', '')
        parts = item.split(' -> ')
        sourceAsymbol = parts[0].split(',')
        state = sourceAsymbol[0].strip('()')
        if state not in nfa:
            nfa[state] = {}
        path = sourceAsymbol[1].strip('()')
        reaching_state = [parts[1].strip('{}')] # '{}' işaretlerini kaldırın
        nfa[state][path] = reaching_state
        aNfa[(state, path)] = reaching_state
    
    df = pd.DataFrame(nfa).transpose().fillna(' ')
   
    print(df)
    print(nfa)
    return nfa,aNfa
        
def draw_dfa_graph(gecisler):
    dot = Digraph(comment='Regex Otomatonu')
    states = set()
    for gecis in gecisler:
        parts = gecis.split(' -> ')
        if len(parts) != 2:
            print("Geçersiz geçiş ifadesi:", gecis)
            continue
        durum, sembol = parts[0][1:-1].split(', ')
        hedef_durumlar = parts[1].split(', ')
        for hedef_durum in hedef_durumlar:
            states.add(durum)
            states.add(hedef_durum)
            dot.edge(durum, hedef_durum, label=sembol)
    for state in states:
        if state == gecisler[-1].split(' -> ')[-1]:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)
    return dot

if __name__ == "__main__":
    kullanıcı_regex = regex_al()
    ifade_listesi = ifadeyi_listeye_ayır(kullanıcı_regex)
    print(ifade_listesi)
    baslangic_durumu = "q0"
    hedef_durum = "qh" 
    print('start state: ' + baslangic_durumu)
    gecisler = regex_gecisleri_olustur(ifade_listesi, baslangic_durumu, hedef_durum)
    for gecis in gecisler:
        print("\u03B4:", gecis)
    final = gecisler[-1].split(' -> ')[-1]
    print('final state: ' + final)
    graph = draw_regex_graph(gecisler)
    graph.render('regex_graph', format='png', cleanup=True)
    graph.view()
    optimize=optimize_transitions(gecisler)
    print("--------NFA Geçişleri--------")
    for gecis in optimize:
        print("\u03B4:", gecis)
    print("--------NFA Tablosu--------")
    nfa,aNfa=tabloOlustur(optimize)

 