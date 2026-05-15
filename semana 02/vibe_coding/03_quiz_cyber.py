#!/usr/bin/env python3
import sys
import time

from typing import List, Optional, Tuple


def timed_input(prompt: str, timeout: float) -> Optional[str]:
    if sys.platform.startswith('win'):
        try:
            import msvcrt
        except ImportError:
            pass
        else:
            print(prompt, end='', flush=True)
            line = ''
            start = time.time()
            while True:
                if msvcrt.kbhit():
                    char = msvcrt.getwch()
                    if char in '\r\n':
                        print()
                        return line
                    if char == '\003':
                        raise KeyboardInterrupt
                    if char == '\b':
                        if line:
                            line = line[:-1]
                            print('\b \b', end='', flush=True)
                    else:
                        line += char
                        print(char, end='', flush=True)
                if time.time() - start >= timeout:
                    print()
                    return None
                time.sleep(0.01)

    # Fallback for non-Windows or if msvcrt isn't available
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(input, prompt)
        try:
            return future.result(timeout=timeout)
        except Exception:
            return None


def ask_question(question: str, options: List[str]) -> int:
    print(question)
    for index, option in enumerate(options, start=1):
        print(f"  {index}. {option}")

    resposta = timed_input("Escolha uma opção (1-3): ", 10.0)
    if resposta is None:
        print("Tempo esgotado. Erro.")
        return -1

    resposta = resposta.strip()
    if resposta in {"1", "2", "3"}:
        return int(resposta) - 1

    print("Resposta inválida. Erro.")
    return -1


def run_quiz(questions: List[Tuple[str, List[str], int]]) -> int:
    acertos = 0
    for pergunta, opcoes, resposta_correta in questions:
        escolha = ask_question(pergunta, opcoes)
        if escolha == resposta_correta:
            print("Correto!\n")
            acertos += 1
        else:
            print(f"Errado. A resposta correta é: {opcoes[resposta_correta]}\n")
    return acertos


def main() -> None:
    questions = [
        (
            "O que significa o termo 'phishing' em cibersegurança?",
            [
                "Envio de e-mails publicitários autorizados",
                "Tentativa de obter dados pessoais por engano",
                "Proteção de rede contra invasões",
            ],
            1,
        ),
        (
            "Qual é a principal função de um firewall?",
            [
                "Bloquear programas desatualizados",
                "Controlar o tráfego entre redes",
                "Criptografar arquivos no disco",
            ],
            1,
        ),
        (
            "O que é autenticação de dois fatores (2FA)?",
            [
                "Usar duas senhas diferentes",
                "Verificar identidade com dois métodos",
                "Mudar a senha a cada dois dias",
            ],
            1,
        ),
        (
            "O que é malware?",
            [
                "Um tipo de rede segura",
                "Um software malicioso",
                "Um protocolo de comunicação",
            ],
            1,
        ),
        (
            "Qual é uma prática segura ao criar senhas?",
            [
                "Usar a mesma senha em todos os sites",
                "Usar senhas longas e únicas",
                "Anotar senhas em papel junto ao computador",
            ],
            1,
        ),
        (
            "O que significa 'VPN'?",
            [
                "Rede Privada Virtual",
                "Verificação Padrão de Navegação",
                "Proteção de Vírus Nacional",
            ],
            0,
        ),
        (
            "Qual medida ajuda a evitar ataques de engenharia social?",
            [
                "Abrir anexos de e-mails desconhecidos",
                "Desconfiar de mensagens urgentes sem verificar",
                "Compartilhar senhas com colegas de trabalho",
            ],
            1,
        ),
        (
            "O que é ransomware?",
            [
                "Software que ajuda na recuperação de arquivos",
                "Um ataque que cifra dados e pede resgate",
                "Um antivírus gratuito",
            ],
            1,
        ),
        (
            "Para que serve a criptografia?",
            [
                "Aumentar a velocidade da internet",
                "Transformar dados para evitar acesso não autorizado",
                "Limpar vírus do sistema",
            ],
            1,
        ),
        (
            "Qual é um sinal de um e-mail falso?",
            [
                "Destinatário conhecido e conteúdo personalizado",
                "Solicitação urgente de dados pessoais",
                "Assinatura digital válida",
            ],
            1,
        ),
    ]

    print("Quiz de Cybersegurança\nResponda 10 perguntas e veja sua pontuação.")
    pontos = run_quiz(questions)

    print(f"Você acertou {pontos} de {len(questions)} perguntas.")
    if pontos >= 3:
        print("Parabéns! Você está aprovado.")
    else:
        print("Você não atingiu a aprovação. Tente novamente.")


if __name__ == '__main__':
    main()
