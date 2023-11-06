import { getCategories } from '../api/kitchen-service.tsx'
import { useQuery } from "@tanstack/react-query";
interface FilterProps {
    onClickHandler: (id: number) => void;
}
export const CategoryImages = () => {
    const { status, data } = useQuery({ queryKey: ["category"], queryFn: getCategories, refetchOnMount: false });
    return (
        <div className='max-w-[1640px] m-auto px-4 py-12'>
            <h1 className='text-orange-600 font-bold text-4xl text-center'>
                Top Rated Menu Items
            </h1>
            {/* Categories */}
            <div className='grid grid-cols-2 md:grid-cols-4 gap-6 py-6'>
                {status === 'success' && data.map((item, index) => (
                    <div
                        key={index}
                        className='bg-gray-100 rounded-lg p-4 flex justify-between items-center'
                    >
                        <h2 className='font-bold sm:text-xl'>{item.name}</h2>
                        <img src={item.image_url} alt={item.name} className='w-20' />
                    </div>
                ))}
            </div>
        </div>
    );
};


export const CategoryFilter = ({ onClickHandler }: FilterProps) => {
    const { status, data } = useQuery({ queryKey: ["category"], queryFn: getCategories, refetchOnMount: false });

    return (
        <>
            {status === 'success' && data?.map((category, index) => (
                <button key={index}
                    onClick={() => onClickHandler(category.id!)}
                    className='btn m-1 border-orange-600 text-orange-600 hover:bg-orange-600 hover:text-white'
                >
                    {category.name}

                </button>
            ))}
        </>
    );
};

