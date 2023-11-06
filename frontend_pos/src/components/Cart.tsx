import { useEffect, useState } from 'react';
import { useCartStore } from '../store/cart';
import { putOrder } from '../api/kitchen-service';
import { v4 as uuidv4 } from 'uuid';
import StatusDialog from './StatusDialog';

interface ChildProps {
    setParentState: React.Dispatch<React.SetStateAction<boolean>>;
}

interface Order {
    meal_id: number;
    item_name: string;
    total_price: number;
    quantity: number;
}

const Cart = (props: ChildProps) => {
    const { cartItems, delMeal, decreaseQty, increaseQty, emptyCart } = useCartStore();

    const [orderData, setOrderData] = useState({
        total: 0,
        isProcessing: false,
        orderId: '',
        orderPut: false,
        ticketno: -1,
        progress: '',
        orderStatus: '',
    });
    const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);

    const openDialog = () => {
        setIsDialogOpen(true);
    };

    const closeDialog = () => {
        setIsDialogOpen(false);
    };


    useEffect(() => {
        const calculateTotal = () => {
            const total = cartItems.reduce((acc, item) => acc + parseFloat(item.meal.price) * item.quantity, 0);
            setOrderData((prevState) => ({ ...prevState, total: parseFloat(total.toFixed(2)) }));
        };
        const initializeProgress = () => {
            if (cartItems.length === 0) {
                setOrderData((prevState) => ({ ...prevState, progress: '0', ticketno: -1, orderPut: false }));
            }
        };
        calculateTotal();
        initializeProgress();
    }, [cartItems]);

    const makeProcess = (progressToAdd: number = 20) => {
        setOrderData((prevState) => {
            const currentProgress = parseFloat(prevState.progress);
            const newProgress = currentProgress + progressToAdd;
            return { ...prevState, progress: `${newProgress}%` };
        });
    };

    const startPutOrder = async () => {
        if (orderData.isProcessing) return;

        setOrderData((prevState) => ({ ...prevState, isProcessing: true }));
        makeProcess();
        for (const status of ["Paying", "Charged", "Puting Order"]) {
            setOrderData((prevState) => ({ ...prevState, orderStatus: status }));
            openDialog()
            await new Promise((resolve) => setTimeout(resolve, 1000));
            makeProcess();
            closeDialog()

        }

        const order_id = uuidv4()
        const order_items: Order[] = cartItems.map((order) => ({
            order_id: order_id,
            meal_id: order.meal.id!,
            item_name: order.meal.item_name,
            total_price: parseFloat(order.meal.price) * order.quantity,
            quantity: order.quantity!,
        }));


        const response = await putOrder(order_items);

        setOrderData((prevState) => ({
            ...prevState,
            orderPut: true,
            // tslint:disable-next-line tslint-rule-name
            ticketno: parseInt(response.ticket),
            isProcessing: false,
        }));
        makeProcess();
        setOrderData((prevState) => ({ ...prevState, orderStatus: 'Order Put' }));
    };

    const onEmptyCart = () => {
        emptyCart();
        setOrderData((prevState) => ({ ...prevState, ticketno: -1, orderStatus: "" }));
        props.setParentState(false);
    };

    return (
        <div className="w-full h-screen flex flex-col">
            <div className="mb-5 h-4 overflow-hidden rounded-full bg-gray-200">
                <div
                    className="h-4 animate-pulse rounded-full bg-gradient-to-r from-green-500 to-blue-500"
                    style={{ width: orderData.progress }}
                ></div>
            </div>
            <div className="overflow-x-auto flex-grow">
                <table className="table">
                    <tbody>
                        {cartItems.map((item) => (
                            <tr key={item.meal.id}>
                                <td>
                                    <img src={item.meal.image_url} width={80} />
                                </td>
                                <td>
                                    <button
                                        className="btn"
                                        disabled={orderData.orderPut}
                                        onClick={() => increaseQty(item.meal.id!)}
                                    >
                                        +
                                    </button>
                                </td>
                                <td>{item.quantity}</td>
                                <td>
                                    <button
                                        className="btn"
                                        disabled={orderData.orderPut}
                                        onClick={() => decreaseQty(item.meal.id!)}
                                    >
                                        -
                                    </button>
                                </td>
                                <td>{(item.meal.price / 100).toLocaleString("en-US", { style: "currency", currency: "CAD" })}</td>
                                <td>{(item.meal.price * item.quantity / 100).toLocaleString("en-US", { style: "currency", currency: "CAD" })}</td>
                                <td>
                                    <button
                                        className="btn"
                                        disabled={orderData.orderPut}
                                        onClick={() => delMeal(item.meal.id!)}
                                    >
                                        X
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <hr />
                <strong>Total: {(orderData.total / 100).toLocaleString("en-US", { style: "currency", currency: "CAD" })}</strong>
                <div className="flex flex-row justify-between mt-10 m-4">
                    {cartItems.length > 0 && (
                        <>
                            <button
                                className="btn btn-lg btn-success text-capitalize mb-10"
                                disabled={orderData.isProcessing || orderData.orderPut}
                                onClick={startPutOrder}
                            >
                                CheckOut
                            </button>
                            <button
                                className="btn btn-lg text-capitalize mb-10"
                                disabled={orderData.isProcessing || orderData.orderPut}
                                onClick={onEmptyCart}
                            >
                                Empty
                            </button>
                        </>
                    )}
                    <button
                        className="btn btn-lg text-capitalize"
                        disabled={orderData.isProcessing || orderData.orderPut}
                        onClick={() => props.setParentState(false)}
                    >
                        Close
                    </button>
                </div>
                <div className="flex justify-center">{orderData.orderStatus}</div>
                {orderData.ticketno > 0 && (
                    <>
                        <strong>Pick-up Number:</strong>
                        <div className="flex justify-center text-9xl">{orderData.ticketno}</div>
                        <div className="flex justify-center ">Ticket Printed</div>
                        <div className="grid mt-10 m-4">
                            <button className="btn btn-lg btn-success" onClick={onEmptyCart}>
                                Done
                            </button>
                        </div>
                    </>
                )}
            </div>
            <StatusDialog isOpen={isDialogOpen} onClose={closeDialog} orderStatus={orderData.orderStatus} />
        </div>
    );
};

export default Cart;

