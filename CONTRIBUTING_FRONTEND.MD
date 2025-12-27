# Contribuire al Frontend di Rescuecom

Il frontend nella repository è rappresentato dalla cartella `templates`. Include file HTML compatibili con Jinja, motore di template simile alle JSP in Java. [Jinja Template Documentation](https://jinja.palletsprojects.com/en/stable/templates/).

Come framework Usiamo Bootstrap. Questo significa che dove possibile si possono usare le classi e componenti "già fatti" di Bootstrap, che dovrebbero velocizzare di molto lo sviluppo. Si possono consultare qui: [https://getbootstrap.com/docs/5.3/getting-started/introduction/](https://getbootstrap.com/docs/5.3/getting-started/introduction/).

Basta fare copia-incolla di esempi e cambiarne il contenuto.

## Creare nuova pagina
Creare un nuovo file `.html` con questo contenuto:
```
{% extends 'base.html' %}

{% block content %}

<p>Contenuto della pagina</p>

{% endblock %}
```

## Visualizzare una pagina per testing
Installare Python se non lo si è già fatto.

Fare `pip install flask` se non lo si è già fatto.

Avviare `template_viewer.py` da `app`. Dalla pagina aperta, scegliere il template da visualizzare.

## Prompt utile
Genera una pagina HTML Jinja che estende `base.html` e ha il contenuto in `{% block content %}`. `base.html` include già head, navbar e footer. Usa Bootstrap 5 e le sue classi già presenti dove possibile. Contenuto della pagina: [Compilare qui]
