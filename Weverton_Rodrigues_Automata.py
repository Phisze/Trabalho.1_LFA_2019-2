# _______________________________________________________________
#                                                                |
#   Nome: Weverton Rodrigues Arnates                             |
#   Matricula: 0015133                                           |
#                                                                |
#    Classe para tratar Automatos Finitos                        |
#                                                                |
#    Esqueleto para o trabalho pratico de 2019-sem2              |
#                                                                |
#    2a versao:                                                  |
#      - corrigidos pequenos bugs                                |
#      - acrescentada prototipagem nos metodos da classe         |
#        .... funciona como se fosse comentario apenas           |
#      - corrigidos metodos: addTransition, isAFD                |
#      - acrescentados e renomeados metodos                      |
#                                                                |
# _______________________________________________________________|
from __future__ import annotations

from builtins import float


class Automata(object):

    @staticmethod
    def __equivalencia(afd: Automata) -> list:
        equivalencia = dict()
        annotations = dict()
        for i in afd.getStates():
            for j in afd.getStates():
                equivalencia.update({(i, j): False})
                annotations.update({(i, j): []})
                if i == j:
                    equivalencia[(i, j)] = False
                    annotations.pop((i, j))
        for i in list(equivalencia.keys()):
            if (i[0] in afd.getFinals() and i[1] not in afd.getFinals()) or (
                    i[1] in afd.getFinals() and i[0] not in afd.getFinals()):
                equivalencia[i] = True
        for i in list(equivalencia.keys()):
            if not equivalencia[i]:
                t1 = afd.getTransitionsFrom(i[0])
                t2 = afd.getTransitionsFrom(i[1])
                if t1 != t2:
                    for j in range(0, len(afd.getAlphabet())):
                        if equivalencia[(t1[j][1][0], t2[j][1][0])]:
                            equivalencia[i] = True
                            equivalencia[(i[1], i[0])] = True
                            break
                        else:
                            annotations[i].append((t1[j][1][0], t2[j][1][0]))
                            annotations[(i[1], i[0])].append((t1[j][1][0], t2[j][1][0]))

        flagW = False
        flagW2 = False
        while not flagW:
            flagW = True
            for i in list(annotations.keys()):
                if not equivalencia[i]:
                    for j in annotations[i]:
                        if equivalencia[j]:
                            equivalencia[i] = True
                            flagW = False
                            break
        estados = list()
        for i in list(equivalencia.keys()):
            if not equivalencia[i]:
                estados.append(i)
        estados_eq = list()
        for i in estados:
            if i[0] != i[1]:
                q = sorted(list(i))
                estados_eq.append(tuple(q))
        estados_eq = list(set(estados_eq))
        return estados_eq

    @staticmethod
    def __multiplica(afd1: Automata, afd2: Automata) -> Automata:
        # auxiliar: monta automato multiplicado
        if not afd1.isAFD() and not afd2.isAFD():
            afd1.__erro("Not AFD")
            return afd1

        if not afd1.isAFDComplete():
            afd1.__erro("AFD1 not complete")
            return afd1

        if not afd2.isAFDComplete():
            afd2.__erro("AFD2 not complete")
            return afd2
        afd3 = Automata()
        i1 = afd1.getInitials()
        i2 = afd2.getInitials()

        for i in range(0, (len(afd1.getStates()))):
            for j in range(0, (len(afd2.getStates()))):
                afd3.addState(str(i + 1) + ', ' + str(j + 1))

        r = list(afd3.getStates().values())
        l = list(afd3.getStates().keys())

        for i in range(0, (len(afd3.getStates()))):
            if r[i] == str(i1[0]) + ', ' + str(i2[0]):
                afd3.setIntial(l[i])

        origem = afd3.getInitials()
        t1 = afd1.getTransitionsFrom(i1[0])
        t2 = afd2.getTransitionsFrom(i2[0])
        origem = origem[0]
        for i in range(0, (len(afd3.getStates()))):
            for j in range(0, len(afd1.getAlphabet())):
                if r[i] == str(t1[j][1][0]) + ', ' + str(t2[j][1][0]):
                    afd3.addTransition(origem, t1[j][0], l[i])
                    break

        tam1 = len(afd1.getStates()) + 1
        tam2 = len(afd2.getStates()) + 1
        c = False
        z = False
        for i in range(1, tam1):
            for j in range(1, tam2):
                t1 = afd1.getTransitionsFrom(i)
                t2 = afd2.getTransitionsFrom(j)
                for k in range(0, len(afd1.getAlphabet())):
                    for lz in range(0, len(afd3.getStates())):
                        if r[lz] == str(t1[k][1][0]) + ', ' + str(t2[k][1][0]):
                            fim = l[lz]
                            c = True
                        if r[lz] == str(i) + ', ' + str(j):
                            origem = l[lz]
                            z = True
                        if c and z:
                            afd3.addTransition(origem, t1[k][0], fim)
                            c = False
                            z = False
        return afd3

    @staticmethod
    def __calcFechoT(afl):
        fecho = list()
        for i in afl.getStates():
            fecho.append((i, i))
            t = afl.getTransitionsFrom(i)
            restart = True
            while restart:
                for j in range(0, len(t)):
                    if t[j][0] == '':
                        for b in t[j][1]:
                            fecho.append((i, b))
                restart = False

        return fecho

    @staticmethod
    def minimize(afd: Automata) -> Automata:
        eq = list()
        eq = afd.__equivalencia(afd)
        flag = False
        for i in eq:
            if i[0] in afd.getInitials():
                flag = True
            t = afd.removeState(i[0])
            if flag:
                afd.setIntial(i[1])
            for j in t:
                afd.addTransition(j[0], j[1], i[1])
        return afd

    @staticmethod
    def union(afd1: Automata, afd2: Automata) -> Automata:
        afd3 = Automata()
        afd3 = afd3.__multiplica(afd1, afd2)
        r = list(afd3.getStates().values())
        l = list(afd3.getStates().keys())
        for i in range(0, len(afd3.getStates())):
            t = r[i].split(", ")
            for j in range(0, len(afd1.getFinals())):
                if int(t[0]) == afd1.getFinals()[j]:
                    afd3.setFinals(l[i])
            for j in range(0, len(afd2.getFinals())):
                if int(t[3]) == afd2.getFinals()[j]:
                    afd3.setFinals(l[i])
        return afd3

    def intercession(afd1: Automata, afd2: Automata) -> Automata:
        afd3 = Automata()
        afd3 = afd3.__multiplica(afd1, afd2)
        r = list(afd3.getStates().values())
        l = list(afd3.getStates().keys())
        q = False
        w = False
        for i in range(0, len(afd3.getStates())):
            q = False
            w = False
            t = r[i].split(", ")
            for j in range(0, len(afd1.getFinals())):
                if int(t[0]) == afd1.getFinals()[j]:
                    q = True
            for j in range(0, len(afd2.getFinals())):
                if int(t[1]) == afd2.getFinals()[j]:
                    w = True
            if q and w:
                afd3.setFinals(l[i])
        return afd3

    @staticmethod
    def diference(afd1: Automata, afd2: Automata) -> Automata:
        # afd1 - afd2
        afd3 = Automata.__multiplica(afd1, afd2)
        r = list(afd3.getStates().values())
        l = list(afd3.getStates().keys())
        q = False
        w = False
        for i in range(0, len(afd3.getStates())):
            q = False
            w = False
            t = r[i].split(", ")
            for j in range(0, len(afd1.getFinals())):
                if int(t[0]) == afd1.getFinals()[j]:
                    q = True
            for j in range(0, len(afd2.getFinals())):
                if int(t[1]) == afd2.getFinals()[j]:
                    w = True
            if q and not w:
                afd3.setFinals(l[i])
        return afd3

    # pensar
    @staticmethod
    def equivalence(afd1: Automata, afd2: Automata) -> Automata:
        afd3 = Automata()
        afd3 = afd1
        tam = len(afd1.getStates())
        for i in afd2.getStates():
            if i in afd2.getInitials() and i in afd2.getFinals():
                afd3.addState(initial=True, final=True)
            elif i in afd2.getInitials():
                afd3.addState(initial=True)
            elif i in afd2.getFinals():
                afd3.addState(final=True)
            else:
                afd3.addState()

        for i in afd2.getStates():
            t = afd2.getTransitionsFrom(i)
            for j in t:
                afd3.addTransition(i + tam, j[0], j[1][0] + tam)

        estados = afd3.__equivalencia(afd3)
        for i in estados:
            if list(i) == afd3.getInitials():
                print("afd1 and afd2 equivalent")
                return afd3
        print("not equivalent")
        return afd3

    @staticmethod
    def convAFN2AFD(afn: Automata):
        if afn.isAFD():
            afn.__erro("Is AFD")
            return afn

        afd = Automata()
        z = list()
        all = list()
        i = afn.getInitials()
        carregamento = list()
        carregamentoS = list()
        all.append(i)
        p = afd.addState(str(i), initial=True)
        z.append(p)
        while len(all) != 0:
            for m in all:
                for y in m:
                    t = afn.getTransitionsFrom(y)
                    for d in t:
                        carregamento.append(d)
            carregamento = sorted(carregamento, key=lambda item: item[0])
            for t in carregamento:
                if len(carregamentoS) > 0:
                    for y in carregamentoS:
                        q = False
                        if t[0] == y[0]:
                            for r in t[1]:
                                if r not in y[1]:
                                    y[1].append(r)
                        else:
                            if len(carregamentoS) != len(afn.getAlphabet()):
                                q = True
                    if q:
                        carregamentoS.append(t)
                else:
                    carregamentoS.append(t)
            n = all[0]
            p = z[0]
            all.remove(n)
            z.remove(p)
            for i in carregamentoS:
                if str(i[1]) in afd.getStates().values():
                    s_val = list(afd.getStates().values())
                    s_key = list(afd.getStates().keys())
                    key = s_key[s_val.index(str(i[1]))]
                    # key = afd.getStates()[]

                    afd.addTransition(p, i[0], key)
                else:
                    x = afd.addState(str(i[1]))
                    # key = afd.getStates()[]

                    afd.addTransition(p, i[0], x)
                    all.append(i[1])
                    z.append(x)
            q = 0
            carregamento.clear()
            carregamentoS.clear()

        for i in range(0, len(s_val)):
            for j in afn.getFinals():
                if str(j) in s_val[i]:
                    if j not in afd.getFinals():
                        afd.setFinals(s_key[i])
        return afd

    @staticmethod
    def convAFLambda2AFN(aflambda: Automata) -> Automata:
        # 1 - Calcular o fecho vazio de cada estado
        # 2 - Cria o mesmo tanto de estados finais não muda
        # 3 - Iniciais fecho vazio do inicial
        # 4 - Ver onde vai chegar com o fecho depois com o cacter do alfabeto
        #   4.1 - Pega o fecho cada um
        #   4.2 - Gasta o alfabeto
        #   4.3 - Vê onde chega
        #   4.4 - Onde chega é uma chegada
        # 5 - Faz as ligações do inicio para a Chegada
        if aflambda.isAFD():
            aflambda.__erro("Is AFD")
            return aflambda

        if not aflambda.hasLambda():
            aflambda.__erro("Not lambda")
            return aflambda
        afn = Automata()
        s = aflambda.getStates()
        f = aflambda.getFinals()
        # 2 OK
        for i in range(0, len(s)):
            if i + 1 in f:
                afn.addState(final=True)
            else:
                afn.addState()
        # 1 OK
        fechoT = Automata().__calcFechoT(aflambda)
        # print(fechoT)

        # 3 OK
        initial = aflambda.getInitials()
        for i in initial:
            for j in range(0, len(fechoT)):
                if i == fechoT[j][0]:
                    afn.setIntial(fechoT[j][1])

        # 4
        ct = list()
        for i in range(0, len(fechoT)):
            t = aflambda.getTransitionsFrom(fechoT[i][1])
            for j in t:
                if j[0] != '':
                    ct.append((fechoT[i][0], j[0], j[1]))
        for i in aflambda.getStates():
            t = aflambda.getTransitionsFrom(i)
            for j in t:
                if j[0] != '':
                    y = 0
                    sai = True
                    for l in j[1]:
                        tl = aflambda.getTransitionsFrom(l)
                        while sai:
                            for m in tl:
                                if m[0] == '':
                                    ct.append((i, j[0], m[1]))
                                    for n in m[1]:
                                        tl = aflambda.getTransitionsFrom(n)
                                    y = 0
                            else:
                                sai = False
        for i in ct:
            for j in i[2]:
                afn.addTransition(i[0], i[1], j)

        return afn

    @staticmethod
    def convAFextended2AFN(afestendido: Automata) -> Automata:
        # 1 - Pega a string com mais de uma letra
        # 2 - Converte em estados o ultimo volta
        if afestendido.isAFD():
            afestendido.__erro("Is AFD")
            return afestendido

        afn = Automata()
        a = afestendido.getAlphabet()
        s = afestendido.getStates()
        q = list()
        for i in range(0, len(s)):
            afn.addState()
            t = afestendido.getTransitionsFrom(i + 1)
            for j in range(0, len(a)):
                q.append((i + 1, t[j][0], t[j][1]))

        for i in range(0, len(q)):
            if len(q[i][1]) > 1:
                cont = 0
                e1 = q[i][0]
                for j in range(0, len(q[i][1])):
                    print(len(q[i][1]))
                    if len(q[i][1]) - 1 != cont:
                        e2 = afn.addState()
                        afn.addTransition(e1, q[j][1], e2)
                        e1 = e2
                        cont += 1
                    else:
                        for w in q[i][2]:
                            afn.addTransition(e1, q[i][1][len(q[i][1]) - 1], w)
            else:
                for w in q[i][2]:
                    afn.addTransition(q[i][0], q[i][1], w)

        i = afestendido.getInitials()
        for j in range(0, len(i)):
            afn.setIntial(i[j])

        f = afestendido.getFinals()
        for i in range(0, len(f)):
            afn.setFinals(f[i])

        return afn

    @staticmethod
    def convAFD2ER(afd: Automata) -> str:

        if not afd.isAFD():
            afd.__erro("Is not AFD")
            return afd

        tr = Automata()
        cont = 2
        for i in range(0, len(afd.getStates()) + 2):
            if i == 0:
                tr.addState(initial=True)
            elif i == len(afd.getStates()) + 1:
                f = tr.addState(final=True)
            else:
                tr.addState()

        tr.addTransition(1, '', afd.getInitials()[0] + 1)
        for i in afd.getFinals():
            tr.addTransition(i + 1, '', f)

        for i in afd.getStates():
            t = afd.getTransitionsFrom(i)
            for j in t:
                tr.addTransition(i + 1, j[0], j[1][0] + 1)
        regular_expression = ''
        # 2 - Pecorrer se o A incide nele mesmo então A*
        # 3 - Se ele só passar normal então só A
        # 1 - Se com o 2 ou mais letras eles incidirem na mesma letra então (A+B)
        while len(tr.getStates()) != 2:
            t = tr.getTransitionsFrom(cont)

            er_loop = list()
            er_soma = [['-1', -1]]
            er_t = list()
            anterior = ('-1', [-1])
            b = 0
            for i in t:
                if anterior[1][0] == i[1][0]:
                    if er_soma[len(er_soma) - 1][0][b] == anterior[0]:
                        if er_soma[0][0] == -1:
                            er_soma.clear()
                        er_soma[len(er_soma) - 1][0] = er_soma[len(er_soma) - 1][0] + '+' + i[0]
                        b += 2
                    else:
                        if er_soma[0][1] == -1:
                            er_soma.clear()
                        er_soma.append([anterior[0] + '+' + i[0], i[1][0]])
                        if [anterior[0], anterior[1][0]] in er_t:
                            er_t.remove([anterior[0], anterior[1][0]])
                        elif [anterior[0] + '*'] in er_loop:
                            er_loop.remove([anterior[0] + '*'])
                        b = 2
                elif cont == i[1][0]:
                    er_loop.append([i[0] + '*'])
                else:
                    er_t.append([i[0], i[1][0]])

                anterior = i

            # Tirar o estado 'cont' do automato
            for p in er_soma:
                if cont == p[1]:
                    er_soma.remove(p)
                    loop = ['(' + p[0] + ')*']
                    er_loop.append(loop)

            er_f = list()
            if er_soma:
                if er_soma[0][1] == -1:
                    er_soma.clear()
            flag_t = False
            flag_soma = False
            if len(er_loop) > 0:
                for q in er_loop:
                    for w in er_t:
                        er_f.append([q[0] + '' + w[0], w[1]])
                        flag_t = True
                        # er_t.remove(w)
                    for w in er_soma:
                        er_f.append([q[0] + '' + '(' + w[0] + ')', w[1]])
                        flag_soma = True
                        # er_soma.remove(w)

            if flag_soma:
                er_soma.clear()

            if flag_t:
                er_t.clear()

            if len(er_soma) > 0:
                for w in er_soma:
                    er_f.append(['(' + w[0] + ')', w[1]])
            if len(er_t) > 0:
                for w in er_t:
                    er_f.append([w[0], w[1]])

            states = tr.removeState(cont)
            for state in states:
                for er in er_f:
                    tr.addTransition(state[0], state[1] + '' + er[0], er[1])
            cont += 1
            regular_expression = ''
            if len(tr.getStates()) == 2:
                t = tr.getTransitionsFrom(1)
                for f in t:
                    if regular_expression == '':
                        regular_expression = f[0]
                    else:
                        regular_expression = regular_expression + '+' + f[0]
        return regular_expression

    # --------------------------
    #   classe
    # --------------------------

    def __init__(self):
        self.__numEstados = 0

        # --- elementos da quintupla
        self.__estados = dict()  # { E : A*, ... }
        self.__alfabeto = list()  # [ A, ... ]
        self.__fTransicao = dict()  # { (E, A*) : E+, ... }
        self.__iniciais = list()  # [ E, ... ]
        self.__finais = list()  # [ E, ... ]

    def __getNew(self):
        self.__numEstados = self.__numEstados + 1
        return self.__numEstados

    def addState(self, name='', initial=False, final=False):
        novo = self.__getNew()
        self.__estados[novo] = name
        if initial:
            self.__iniciais.append(novo)
        if final:
            self.__finais.append(novo)
        return novo

    def addTransition(self, origem, palavra, destino):
        if not origem in self.__estados or not destino in self.__estados:
            self.__erro('addTransition')
        for c in palavra:
            if not c in self.__alfabeto:
                self.__alfabeto.append(c)
        if (origem, palavra) in self.__fTransicao:
            aux = self.__fTransicao[(origem, palavra)]
        else:
            aux = []
        if not destino in aux:
            self.__fTransicao[(origem, palavra)] = aux + [destino]

    def getInitials(self):
        return self.__iniciais

    def getFinals(self):
        return self.__finais

    def getStates(self):
        return self.__estados

    def getAlphabet(self):
        return self.__alfabeto

    def getTransitionsFrom(self, estado):
        resp = list()
        for (e, s) in self.__fTransicao:
            if e == estado:
                resp.append([s, self.__fTransicao[(e, s)]])
        resp = sorted(resp, key=lambda item: item[0])
        return resp

    def __erro(self, msg):
        print('ERRO: %s' % msg)
        quit()

    def setIntial(self, e):
        self.__iniciais.append(e)

    def setFinals(self, e):
        self.__finais.append(e)

    def removeState(self, state):
        estados = list()
        for i in self.__estados:
            t = self.getTransitionsFrom(i)
            for j in t:
                if i == state:
                    self.__fTransicao.pop((i, j[0]))
                elif j[1][0] == state:
                    estados.append([i, j[0]])
                    self.__fTransicao.pop((i, j[0]))
        if state in self.__finais:
            self.__finais.remove(state)
        if state in self.__iniciais:
            self.__iniciais.remove(state)
        self.__estados.pop(state)
        self.__numEstados -= 1
        y = 0
        return estados

    # ------------------------------------------

    def moveAFD(self, estado, palavra):
        if not self.isAFD():
            self.__erro('moveAFD')
        e = estado
        for a in palavra:
            if not (e, a) in self.__fTransicao:
                return None
            lista = self.__fTransicao[(e, a)]
            e = lista[0]
        return e

    def accept(self, palavra):
        if not self.isAFD():
            self.__erro('accept')
        e = self.moveAFD(self.__iniciais[0], palavra)
        if e is None:
            return False
        else:
            return e in self.__finais

    def isAFD(self):
        if len(self.__iniciais) > 1:
            return False
        for e in self.getStates():
            for (s, destino) in self.getTransitionsFrom(e):
                if len(s) != 1 or len(destino) != 1:
                    return False
        return True

    def hasLambda(self):
        for (e, s) in self.__fTransicao:
            if s == '':
                return True
        return False

    def isAFDComplete(self):
        if not self.isAFD():
            return False
        for e in self.getStates():
            for s in self.getAlphabet():
                if not (e, s) in self.__fTransicao:
                    return False
        return True

    def __str__(self):
        msg = '(E, A, ft, I, F) onde:\n' + \
              '  E  = {0}\n' + \
              '  A  = {1}\n' + \
              '  I  = {3}\n' + \
              '  F  = {4}\n' + \
              '  ft = {2}'
        ft = '{\n'
        for (e, a) in self.__fTransicao:
            t = self.__fTransicao[(e, a)]
            ft = '{0}    ({1}, {2}): {3},\n'.format(ft, e, a, t)
        ft = ft + '  }'
        return msg.format(self.__estados, \
                          self.__alfabeto, ft, \
                          self.__iniciais, self.__finais)


if __name__ == "__main__":

    # multiplicacao
    af = Automata()

    e1 = af.addState(initial=True, final=True)
    e2 = af.addState()
    af.addTransition(1, 'a', 2)
    af.addTransition(2, 'a', 1)
    af.addTransition(e1, 'b', e1)
    af.addTransition(e2, 'b', e2)

    af1 = Automata()

    e3 = af1.addState(initial=True, final=True)
    e4 = af1.addState()
    af1.addTransition(e3, 'a', e3)
    af1.addTransition(e4, 'a', e4)
    af1.addTransition(e3, 'b', e4)
    af1.addTransition(e4, 'b', e3)
    q = af1.getTransitionsFrom(e3)

    afd = Automata()

    # afd = Automata.diference(af, af1)
    # print(afd)

    afn = Automata()

    v1 = afn.addState(initial=True, final=True)
    v2 = afn.addState(initial=True)
    v3 = afn.addState()
    v4 = afn.addState(final=True)
    afn.addTransition(v1, 'a', v2)
    afn.addTransition(v1, 'a', v3)
    afn.addTransition(v2, 'a', v2)
    afn.addTransition(v2, 'b', v4)
    afn.addTransition(v3, 'b', v3)
    # afn.addTransition(v3, '', v4)
    afn.addTransition(v3, 'b', v1)

    af = afn.convAFN2AFD(afn)
    # t = afn.convAFD2ER(af)
    # print(af)
    # a = afn.convAFLambda2AFN(afn)
    # print(afn)
    # print(a)
    # AFL TO AFN
    afl = Automata()
    l1 = afl.addState(initial=True)
    l2 = afl.addState(final=True)
    l3 = afl.addState()
    l4 = afl.addState()

    afl.addTransition(l1, 'a', l1)
    afl.addTransition(l1, '', l2)
    afl.addTransition(l2, 'a', l3)
    afl.addTransition(l2, 'b', l2)
    afl.addTransition(l2, '', l4)
    afl.addTransition(l3, 'b', l1)
    afl.addTransition(l4, 'a', l4)
    afl.addTransition(l4, 'b', l4)
    afl.addTransition(l4, '', l3)

    afP = Automata()
    p1 = afP.addState(initial=True)
    p2 = afP.addState()
    p3 = afP.addState()
    p4 = afP.addState(final=True)

    afP.addTransition(p1, '', p2)
    afP.addTransition(p1, 'a', p3)
    afP.addTransition(p2, 'a', p2)
    afP.addTransition(p2, 'b', p4)
    afP.addTransition(p3, 'b', p3)
    afP.addTransition(p3, '', p4)
    afP.addTransition(p4, 'c', p4)
    afd1 = Automata()
    # afd1 = afd1.convAFLambda2AFN(afP)
    # print(afd1)

    af = Automata()

    e1 = af.addState(initial=True, final=True)
    e2 = af.addState()
    af.addTransition(e1, 'a', e2)
    af.addTransition(e2, 'a', e1)
    af.addTransition(e1, 'b', e1)
    af.addTransition(e2, 'b', e2)

    afe = Automata()
    ae1 = afe.addState()
    ae2 = afe.addState(initial=True, final=True)
    afe.addTransition(ae1, 'a', ae1)
    afe.addTransition(ae1, 'b', ae2)
    afe.addTransition(ae2, 'b', ae1)
    afe.addTransition(ae2, 'aba', ae2)

    # afne = Automata()
    # afne = afne.convAFextended2AFN(afe)
    # print(afne)
    # AFN to AFD
    afn = Automata()
    an1 = afn.addState(initial=True)
    an2 = afn.addState(final=True)
    afn.addTransition(an1, 'a', an1)
    afn.addTransition(an1, 'b', an1)
    afn.addTransition(an1, 'a', an2)

    # q = afn.convAFN2AFD(afn)
    # print(q)

    t2 = Automata()
    q0 = t2.addState(initial=True, final=True)
    q1 = t2.addState(final=True)
    q2 = t2.addState()
    q3 = t2.addState()
    q4 = t2.addState()

    t2.addTransition(q0, 'a', q1)
    t2.addTransition(q0, 'a', q2)
    t2.addTransition(q1, 'a', q1)
    t2.addTransition(q1, 'a', q2)
    t2.addTransition(q2, 'b', q3)
    t2.addTransition(q2, 'b', q4)
    t2.addTransition(q3, 'a', q1)
    t2.addTransition(q3, 'b', q3)
    t2.addTransition(q3, 'b', q4)
    # t = t2.convAFN2AFD(t2)
    # print(t)

    # AFD to ER
    er = Automata()
    q1 = er.addState(initial=True, final=True)
    q2 = er.addState()
    q3 = er.addState(final=True)

    er.addTransition(q1, '0', q1)
    er.addTransition(q1, '1', q2)
    er.addTransition(q2, '0', q2)
    er.addTransition(q2, '1', q3)
    er.addTransition(q3, '0', q3)
    er.addTransition(q3, '1', q3)
    # er.removeState(q2)
    # t = er.convAFD2ER(er)
    # print(t)

    er = Automata()
    q1 = er.addState(initial=True)
    q2 = er.addState(final=True)

    er.addTransition(q1, 'a', q2)
    er.addTransition(q1, 'b', q2)
    er.addTransition(q1, 'c', q2)

    er.addTransition(q1, 'd', q1)
    er.addTransition(q1, 'e', q1)
    er.addTransition(q1, 'f', q1)

    # t = er.convAFD2ER(er)
    # print(t)
    afM = Automata()
    m0 = afM.addState(initial=True, final=True)
    m1 = afM.addState()
    m2 = afM.addState()
    m3 = afM.addState()
    m4 = afM.addState()
    m5 = afM.addState()
    afM.addTransition(m0, 'a', m0)
    afM.addTransition(m0, 'b', m1)
    afM.addTransition(m1, 'a', m2)
    afM.addTransition(m1, 'b', m3)
    afM.addTransition(m2, 'a', m4)
    afM.addTransition(m2, 'b', m5)
    afM.addTransition(m3, 'a', m0)
    afM.addTransition(m3, 'b', m1)
    afM.addTransition(m4, 'a', m2)
    afM.addTransition(m4, 'b', m3)
    afM.addTransition(m5, 'a', m4)
    afM.addTransition(m5, 'b', m5)

    afN = Automata()

    q0 = afN.addState(initial=True)
    q1 = afN.addState(final=True)
    q2 = afN.addState()
    q3 = afN.addState()
    d = afN.addState()

    afN.addTransition(q0, '0', q1)
    afN.addTransition(q0, '1', d)
    afN.addTransition(q1, '0', q2)
    afN.addTransition(q1, '1', q3)
    afN.addTransition(q2, '1', d)
    afN.addTransition(q2, '0', q1)
    afN.addTransition(q3, '0', d)
    afN.addTransition(q3, '1', q1)
    afN.addTransition(d, '0', d)
    afN.addTransition(d, '1', d)

    # a = Automata()
    # a = a.minimize(afM)
    # print(a)

    afE1 = Automata()
    a1 = afE1.addState(initial=True)
    a2 = afE1.addState(final=True)
    afE1.addTransition(a1, 'a', a2)
    afE1.addTransition(a1, 'b', a1)
    afE1.addTransition(a2, 'a', a1)
    afE1.addTransition(a2, 'b', a2)
    print(afE1.convAFD2ER(afE1))
    afE2 = Automata()
    a1 = afE2.addState(final=True)
    a2 = afE2.addState(initial=True)
    afE2.addTransition(a1, 'a', a2)
    afE2.addTransition(a1, 'b', a1)
    afE2.addTransition(a2, 'a', a1)
    afE2.addTransition(a2, 'b', a2)

    at = Automata()
    at.equivalence(afE1, afE2)

    # at.equi(afM)
    afSort = Automata()
    q0 = afSort.addState(initial=True)
    q1 = afSort.addState(final=True)

    afSort.addTransition(q0, 'a', q1)
    afSort.addTransition(q0, 'b', q0)
    afSort.addTransition(q1, 'b', q0)
    afSort.addTransition(q1, 'a', q1)

    # print(afSort.getTransitionsFrom(2))

    af5 = Automata()
    e1 = af5.addState('1', initial=True, final=True)
    e2 = af5.addState('2', final=True)
    e3 = af5.addState('3')
    e4 = af5.addState('4', final=True)
    e5 = af5.addState('5', final=True)
    e6 = af5.addState('6')
    af5.addTransition(e1, 'a', e2)
    af5.addTransition(e1, 'b', e6)
    af5.addTransition(e2, 'a', e2)
    af5.addTransition(e2, 'b', e3)
    af5.addTransition(e3, 'a', e4)
    af5.addTransition(e3, 'b', e3)
    af5.addTransition(e4, 'a', e5)
    af5.addTransition(e4, 'b', e6)
    af5.addTransition(e5, 'a', e5)
    af5.addTransition(e5, 'b', e3)
    af5.addTransition(e6, 'a', e6)
    af5.addTransition(e6, 'b', e6)

    # at = Automata()
    # q = at.equi(afM)
    # print(q)
    # print("M5 = ", af5)

    # print(afe)
    # print(a)
    # print('M2 = ', af)
    # print('\noutros testes:')
    while True:
        w = 'Digite uma palavra no alfabeto {0} ou PARE para terminar: '
        s = input(w.format(af.getAlphabet()))
        if s == 'PARE':
            break
        r = af.accept(s)
        print('Aceita a palavra "{0}"? --> {1}'.format(s, r))
    print('Fim dos testes.')
