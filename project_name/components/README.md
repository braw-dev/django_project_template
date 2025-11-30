# Django components

Example component in `templates/components/card.html`

```text
<div class="bg-white shadow rounded border p-4">
    <h2>{% templatetag openvariable %} title {% templatetag closevariable %}</h2>
    <p>{% templatetag openvariable %} slot {% templatetag closevariable %}</p>
    <button href="{% templatetag openblock %} url url {% templatetag closeblock %}">Read more</button>
</div>
```

And how to use it:

```text
<c-card title="Trees" url="trees">
    We have the best trees
</c-card>
```

## Usage

Taken from the [django-cotton docs](https://django-cotton.com/docs/quickstart#usage).

## Naming

Cotton uses the following naming conventions:

- Component file names are in snake_case: my_component.html
- but are called using kebab-case: <c-my-component />

## Subfolders

- Components in subfolders can be defined using dot notation
- A component in sidebar/menu/link.html would be included as <c-sidebar.menu.link />

## Tag Style

- Components can either be self-closing <c-my-component /> or have a closing tag <c-my-component></c-my-component>
