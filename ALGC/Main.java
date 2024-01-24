class Main {
    public static void printArray(int[] array, int index) {
        if (index == array.length) {
            return;
        }

        System.out.println(array[index]);
        printArray(array, index + 1);
    }

    public static void triSelection(int[] array, int index) {
        if (index == array.length) {
            return;
        }

        int min = index;
        for (int i = index; i < array.length; i++) {
            if (array[i] < array[min]) {
                min = i;
            }
        }

        int tmp = array[index];
        array[index] = array[min];
        array[min] = tmp;

        triSelection(array, index + 1);
    }
    
    public static void main(String[] args) {
        int array[] = { 1, 2, 3, 4, 5 };

        printArray(array, 0);
    }
}