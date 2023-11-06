import { queryOrder } from '../api/kitchen-service';
import { useRef, useState } from 'react';
import StatusDialog from './StatusDialog';

interface Response {
    order_status: string;
}

export const SearchBar: React.FC = () => {
    const ticket = useRef<HTMLInputElement | null>(null);
    const [orderStatus, setOrderStatus] = useState<string>('');
    const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);

    const openDialog = () => {
        setIsDialogOpen(true);
    };

    const closeDialog = () => {
        setIsDialogOpen(false);
    };

    const handleSearch = async () => {
        if (ticket.current) {
            const response: Response = await queryOrder(parseInt(ticket.current.value));
            if (response.order_status !== "{}") {
                setOrderStatus(response.order_status);
            } else {
                setOrderStatus("Order Not Found")
            }
            openDialog();
        }
    };

    return (
        <div className="relative max-w-sm mx-auto">
            <input
                type="number"
                ref={ticket}
                className="w-full py-2 px-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Search"
            />
            <button
                className="absolute inset-y-0 right-0 flex items-center px-4 text-gray-700 bg-gray-100 border border-gray-300 rounded-r-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                onClick={handleSearch}
            >
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fillRule="evenodd" clipRule="evenodd" d="M14.795 13.408l5.204 5.204a1 1 0 01-1.414 1.414l-5.204-5.204a7.5 7.5 0 111.414-1.414zM8.5 14A5.5 5.5 0 103 8.5 5.506 5.506 0 008.5 14z" />
                </svg>
            </button>
            <StatusDialog isOpen={isDialogOpen} onClose={closeDialog} orderStatus={orderStatus} />
        </div>
    );
};


