document.getElementById('add').addEventListener('click', () => {
    change_ingredients_quantity('u')
})
document.getElementById('subtract').addEventListener('click', () => {
    change_ingredients_quantity('d')
})
function change_ingredients_quantity(up_or_down) {
    let slug = '{{recipe.slug}}';
    let add_button = document.getElementById('add');
    let subtract_button = document.getElementById('subtract');
    let num_of_dishes; 
    let ingredientTag;
    if (up_or_down == 'u') {
        num_of_dishes = parseInt(add_button.getAttribute('value')) + 1;
    } else {
        num_of_dishes = parseInt(add_button.getAttribute('value')) - 1;
    }
    if (num_of_dishes <= 0) {
        return
    }
    add_button.setAttribute('value', num_of_dishes);
    subtract_button.setAttribute('value', num_of_dishes);
    fetch(`/api/get_num_of_dishes/${slug}/${num_of_dishes}/`)
        .then(response => response.json())
        .then(function(data) {
            for (let i=0; i < data.length; i++) {
                ingredientTag = document.getElementById(`ingredient-${i}`);
                qty = ingredientTag.getElementsByClassName('ing-quantity')[0];
                qty.innerHTML = data[i];
                console.log(data[i]);
            }
        })
        .catch(error => console.log(error))
}

