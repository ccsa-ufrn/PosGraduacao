/* Altera a visibilidade de um objeto, bastando passar o id dele.
    O objeto deve estar por padrão setado com style "" ou "display: none".
    PS: style null != style ""
    
    README: gambiarra temporária
    TODO: evitar fazer isso em casa */

function alternar(idDetalhes){
    var objDetalhes = document.getElementById(idDetalhes);

    var isVisivel = objDetalhes.getAttribute("style") == "";

    objDetalhes.setAttribute("style", (isVisivel ? "display: none" : ""));
    return false;
}