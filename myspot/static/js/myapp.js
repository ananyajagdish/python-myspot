function setSelection(s, v) {
    hiddenInput = document.getElementById("selectedid");
    hiddenInput.value = v;
    const parentElement = document.getElementById("selectionContainer");
    const childElements = parentElement.children;

    for (let i = 0; i < childElements.length; i++) {
        childElements[i].classList = null;
        if (childElements[i].id == s) {
            childElements[i].classList.add("selected");
        } else {
            childElements[i].classList.add("selection");
        }
    }
}

function validateAndSubmitSelection() {
    hiddenInput = document.getElementById("selectedid");
    if (hiddenInput.value != "") {
        document.getElementById("selectionForm").submit();
    }
}