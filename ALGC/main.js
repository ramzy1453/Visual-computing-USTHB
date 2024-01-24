console.clear();

const array = [8, 9, 3, 5, 7, 4, 2, 1];

function triSelection(arr) {
  const n = arr.length;
  for (let i = 0; i < n; i++) {
    let min = array[i];
    for (let j = i + 1; j < n; j++) {
      if (arr[j] < min) {
        console.log("min : ", min, "array", arr, "i", i, "j", j);
        min = array[j];
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
    }
  }

  return arr;
}

function triInsertion(arr, n) {
  for (let i = 1; i < n; i++) {
    let currentValue = arr[i];
    let j;
    for (j = i - 1; j >= 0 && arr[j] > currentValue; j--) {
      arr[j + 1] = arr[j];
    }
    arr[j + 1] = currentValue;
  }
  return arr;
}

function triBulle(arr, n) {
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n - i; j++) {
      if (arr[j + 1] < arr[j]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
      }
    }
  }
  return arr;
}

function triRapide(arr) {
  const n = arr.length;

  if (n <= 1) {
    return arr;
  }

  let pivot = arr[0];
  let left = [];
  let right = [];

  for (let i = 1; i < n; i++) {
    if (arr[i] < pivot) {
      left.push(arr[i]);
    } else {
      right.push(arr[i]);
    }
  }
  return [...triRapide(left), pivot, ...triRapide(right)];
}

// Fonction principale pour trier un tableau en utilisant le tri par tas
function triParTas(arr) {
  const n = arr.length;

  // Construire un tas (réorganiser le tableau)
  for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
    entretienTas(arr, n, i);
  }

  // Extraire un par un les éléments du tas
  for (let i = n - 1; i > 0; i--) {
    // Déplacer la racine actuelle à la fin
    [arr[0], arr[i]] = [arr[i], arr[0]];

    // Appeler la fonction entretienTas sur le tas réduit
    entretienTas(arr, i, 0);
  }

  return arr;
}

// Fonction pour réorganiser le tas
function entretienTas(arr, n, i) {
  let plusGrand = i;
  const gauche = 2 * i;
  const droite = 2 * i + 1;

  // Si le fils gauche est plus grand que la racine
  if (gauche < n && arr[gauche] > arr[plusGrand]) {
    plusGrand = gauche;
  }

  // Si le fils droit est plus grand que le plus grand jusqu'à présent
  if (droite < n && arr[droite] > arr[plusGrand]) {
    plusGrand = droite;
  }

  // Si le plus grand n'est pas la racine
  if (plusGrand !== i) {
    // Échanger avec le plus grand et continuer à entretienTas
    [arr[i], arr[plusGrand]] = [arr[plusGrand], arr[i]];
    entretienTas(arr, n, plusGrand);
  }
}

function divide(arr) {
  const n = arr.length;

  if (n === 1) return arr;

  if (n === 2) {
    if (arr[1] < arr[0]) {
      [arr[0], arr[1]] = [arr[1], arr[0]];
    }
  }

  let left = [];
  let right = [];

  for (let i = 0; i < n; i++) {
    if (i < n / 2) left.push(arr[i]);
    else right.push(arr[i]);
  }

  return [...divide(left), ...divide(right)];
}

function merge(arr) {
  const n = arr.length;
  console.log(n);
  if (n === 1) {
    return arr;
  }
  // dim
  console.log(arr[0].length, "ok");

  return [...merge(arr[0]), ...merge(arr[1])];
}

const divided = divide(array);

console.log(merge(divided));
