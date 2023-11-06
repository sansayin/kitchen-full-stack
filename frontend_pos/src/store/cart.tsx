import { create } from "zustand";
import { Menu } from "../generated/models/Menu";

const loadCartItems = () => {
    const storedCartItems = localStorage.getItem("cartItems");
    return storedCartItems ? JSON.parse(storedCartItems) : [];
};

interface Order {
    meal: Menu
    quantity: number
}

type OrderStore = {
    cartItems: Order[],
    addMeal: (product: Menu) => void
    delMeal: (productId: number) => void
    decreaseQty: (productId: number) => void
    increaseQty: (productId: number) => void
    emptyCart: () => void
}

export const useCartStore = create<OrderStore>((set) => ({
    cartItems: loadCartItems(),
    addMeal: (product: Menu) => {
        set((state) => {
            const itemIndex = state.cartItems.findIndex((item) => item.meal.id === product.id)
            if (itemIndex !== -1) {
                state.cartItems[itemIndex].quantity++
            } else {
                state.cartItems.push({ meal: product, quantity: 1 })
            }
            localStorage.setItem("cartItems", JSON.stringify(state.cartItems));
            return {
                cartItems: [...state.cartItems]
            }
        })
    },
    delMeal: (productId: number) => {
        set((state) => {
            const updatedCartItems = state.cartItems.filter((item) => item.meal.id != productId)
            localStorage.setItem("cartItems", JSON.stringify(updatedCartItems));
            return {
                cartItems: updatedCartItems
            }
        })
    },
    increaseQty: (productId: number) => {
        set((state) => {
            const updatedCartItems = state.cartItems.map((item) => {
                if (item.meal.id === productId) {
                    return { ...item, quantity: item.quantity + 1 };
                }
                return item;
            });
            localStorage.setItem("cartItems", JSON.stringify(updatedCartItems));
            return {
                cartItems: updatedCartItems
            };

        });
    },

    decreaseQty: (productId: number) => {
        set((state) => {
            const updatedCartItems = state.cartItems.map((item) => {
                if (item.meal.id === productId) {
                    return { ...item, quantity: item.quantity - 1 };
                }
                return item;
            });
            const filteredCartItems = updatedCartItems.filter((item) => item.quantity > 0);
            localStorage.setItem("cartItems", JSON.stringify(filteredCartItems));
            return {
                cartItems: filteredCartItems,
            };

        });
    },
    emptyCart: () => {
        set(() => {
            localStorage.removeItem('cartItems');
            return {
                cartItems: []
            };
        });
    }
}))
