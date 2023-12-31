import string
import random

letters = string.ascii_letters + string.punctuation + string.digits

def shuffle():
    global letters
    chars = [char for char in letters]
    for _ in range(100):
        random.shuffle(chars)

    return ''.join(chars)

SECRET_KEY = shuffle()
 

COUNTRIES = (
    ('Afeganistão', 'Afeganistão'),
    ('África do Sul', 'África do Sul'),
    ('Albânia', 'Albânia'),
    ('Alemanha', 'Alemanha'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Antiga e Barbuda', 'Antiga e Barbuda'),
    ('Arábia Saudita', 'Arábia Saudita'),
    ('Argélia', 'Argélia'),
    ('Argentina', 'Argentina'),
    ('Arménia', 'Arménia'),
    ('Austrália', 'Austrália'),
    ('Áustria', 'Áustria'),
    ('Azerbaijão', 'Azerbaijão'),
    ('Bahamas', 'Bahamas'),
    ('Bangladexe', 'Bangladexe'),
    ('Barbados', 'Barbados'),
    ('Barém', 'Barém'),
    ('Bélgica', 'Bélgica'),
    ('Belize', 'Belize'),
    ('Benim', 'Benim'),
    ('Bielorrússia', 'Bielorrússia'),
    ('Bolívia', 'Bolívia'),
    ('Bósnia e Herzegovina', 'Bósnia e Herzegovina'),
    ('Botsuana', 'Botsuana'),
    ('Brasil', 'Brasil'),
    ('Brunei', 'Brunei'),
    ('Bulgária', 'Bulgária'),
    ('Burquina Faso', 'Burquina Faso'),
    ('Burúndi', 'Burúndi'),
    ('Butão', 'Butão'),
    ('Cabo Verde', 'Cabo Verde'),
    ('Camarões', 'Camarões'),
    ('Camboja', 'Camboja'),
    ('Canadá', 'Canadá'),
    ('Catar', 'Catar'),
    ('Cazaquistão', 'Cazaquistão'),
    ('Chade', 'Chade'),
    ('Chile', 'Chile'),
    ('China', 'China'),
    ('Chipre', 'Chipre'),
    ('Colômbia', 'Colômbia'),
    ('Comores', 'Comores'),
    ('Congo-Brazzaville', 'Congo-Brazzaville'),
    ('Coreia do Norte', 'Coreia do Norte'),
    ('Coreia do Sul', 'Coreia do Sul'),
    ('Cosovo', 'Cosovo'),
    ('Costa do Marfim', 'Costa do Marfim'),
    ('Costa Rica', 'Costa Rica'),
    ('Croácia', 'Croácia'),
    ('Cuaite', 'Cuaite'),
    ('Cuba', 'Cuba'),
    ('Dinamarca', 'Dinamarca'),
    ('Dominica', 'Dominica'),
    ('Egito', 'Egito'),
    ('Emirados Árabes Unidos', 'Emirados Árabes Unidos'),
    ('Equador', 'Equador'),
    ('Eritreia', 'Eritreia'),
    ('Eslováquia', 'Eslováquia'),
    ('Eslovénia', 'Eslovénia'),
    ('Espanha', 'Espanha'),
    ('Essuatíni', 'Essuatíni'),
    ('Estado da Palestina', 'Estado da Palestina'),
    ('Estados Unidos da América', 'Estados Unidos da América'),
    ('Estónia', 'Estónia'),
    ('Etiópia', 'Etiópia'),
    ('Fiji', 'Fiji'),
    ('Filipinas', 'Filipinas'),
    ('Finlândia', 'Finlândia'),
    ('França', 'França'),
    ('Gabão', 'Gabão'),
    ('Gâmbia', 'Gâmbia'),
    ('Gana', 'Gana'),
    ('Geórgia', 'Geórgia'),
    ('Granada', 'Granada'),
    ('Grécia', 'Grécia'),
    ('Guatemala', 'Guatemala'),
    ('Guiana', 'Guiana'),
    ('Guiné', 'Guiné'),
    ('Guiné Equatorial', 'Guiné Equatorial'),
    ('Guiné-Bissau', 'Guiné-Bissau'),
    ('Haiti', 'Haiti'),
    ('Honduras', 'Honduras'),
    ('Hungria', 'Hungria'),
    ('Iémen', 'Iémen'),
    ('Ilhas Marechal', 'Ilhas Marechal'),
    ('Índia', 'Índia'),
    ('Indonésia', 'Indonésia'),
    ('Irão', 'Irão'),
    ('Iraque', 'Iraque'),
    ('Irlanda', 'Irlanda'),
    ('Islândia', 'Islândia'),
    ('Israel', 'Israel'),
    ('Itália', 'Itália'),
    ('Jamaica', 'Jamaica'),
    ('Japão', 'Japão'),
    ('Jibuti', 'Jibuti'),
    ('Jordânia', 'Jordânia'),
    ('Laus', 'Laus'),
    ('Lesoto', 'Lesoto'),
    ('Letónia', 'Letónia'),
    ('Líbano', 'Líbano'),
    ('Libéria', 'Libéria'),
    ('Líbia', 'Líbia'),
    ('Listenstaine', 'Listenstaine'),
    ('Lituânia', 'Lituânia'),
    ('Luxemburgo', 'Luxemburgo'),
    ('Macedónia do Norte', 'Macedónia do Norte'),
    ('Madagáscar', 'Madagáscar'),
    ('Malásia', 'Malásia'),
    ('Maláui', 'Maláui'),
    ('Maldivas', 'Maldivas'),
    ('Mali', 'Mali'),
    ('Malta', 'Malta'),
    ('Marrocos', 'Marrocos'),
    ('Maurícia', 'Maurícia'),
    ('Mauritânia', 'Mauritânia'),
    ('México', 'México'),
    ('Mianmar', 'Mianmar'),
    ('Micronésia', 'Micronésia'),
    ('Moçambique', 'Moçambique'),
    ('Moldávia', 'Moldávia'),
    ('Mónaco', 'Mónaco'),
    ('Mongólia', 'Mongólia'),
    ('Montenegro', 'Montenegro'),
    ('Namíbia', 'Namíbia'),
    ('Nauru', 'Nauru'),
    ('Nepal', 'Nepal'),
    ('Nicarágua', 'Nicarágua'),
    ('Níger', 'Níger'),
    ('Nigéria', 'Nigéria'),
    ('Noruega', 'Noruega'),
    ('Nova Zelândia', 'Nova Zelândia'),
    ('Omã', 'Omã'),
    ('Países Baixos', 'Países Baixos'),
    ('Palau', 'Palau'),
    ('Panamá', 'Panamá'),
    ('Papua Nova Guiné', 'Papua Nova Guiné'),
    ('Paquistão', 'Paquistão'),
    ('Paraguai', 'Paraguai'),
    ('Peru', 'Peru'),
    ('Polónia', 'Polónia'),
    ('Portugal', 'Portugal'),
    ('Quénia', 'Quénia'),
    ('Quirguistão', 'Quirguistão'),
    ('Quiribáti', 'Quiribáti'),
    ('Reino Unido', 'Reino Unido'),
    ('República Centro-Africana', 'República Centro-Africana'),
    ('República Checa', 'República Checa'),
    ('República Democrática do Congo', 'República Democrática do Congo'),
    ('República Dominicana', 'República Dominicana'),
    ('Roménia', 'Roménia'),
    ('Ruanda', 'Ruanda'),
    ('Rússia', 'Rússia'),
    ('Salomão', 'Salomão'),
    ('Salvador', 'Salvador'),
    ('Samoa', 'Samoa'),
    ('Santa Lúcia', 'Santa Lúcia'),
    ('São Cristóvão e Neves', 'São Cristóvão e Neves'),
    ('São Marinho', 'São Marinho'),
    ('São Tomé e Príncipe', 'São Tomé e Príncipe'),
    ('São Vicente e Granadinas', 'São Vicente e Granadinas'),
    ('Seicheles', 'Seicheles'),
    ('Senegal', 'Senegal'),
    ('Serra Leoa', 'Serra Leoa'),
    ('Sérvia', 'Sérvia'),
    ('Singapura', 'Singapura'),
    ('Síria', 'Síria'),
    ('Somália', 'Somália'),
    ('Sri Lanca', 'Sri Lanca'),
    ('Sudão', 'Sudão'),
    ('Sudão do Sul', 'Sudão do Sul'),
    ('Suécia', 'Suécia'),
    ('Suíça', 'Suíça'),
    ('Suriname', 'Suriname'),
    ('Tailândia', 'Tailândia'),
    ('Taiuã', 'Taiuã'),
    ('Tajiquistão', 'Tajiquistão'),
    ('Tanzânia', 'Tanzânia'),
    ('Timor-Leste', 'Timor-Leste'),
    ('Togo', 'Togo'),
    ('Tonga', 'Tonga'),
    ('Trindade e Tobago', 'Trindade e Tobago'),
    ('Tunísia', 'Tunísia'),
    ('Turcomenistão', 'Turcomenistão'),
    ('Turquia', 'Turquia'),
    ('Tuvalu', 'Tuvalu'),
    ('Ucrânia', 'Ucrânia'),
    ('Uganda', 'Uganda'),
    ('Uruguai', 'Uruguai'),
    ('Usbequistão', 'Usbequistão'),
    ('Vanuatu', 'Vanuatu'),
    ('Vaticano', 'Vaticano'),
    ('Venezuela', 'Venezuela'),
    ('Vietname', 'Vietname'),
    ('Zâmbia', 'Zâmbia'),
    ('Zimbábue', 'Zimbábue')
)
