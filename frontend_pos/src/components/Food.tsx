import { useEffect, useState } from 'react';
import { getMenu } from '../api/kitchen-service.tsx'
import { useQuery } from "@tanstack/react-query";
import { useCartStore } from '../store/cart';
import { FaPlus } from 'react-icons/fa';
import { CategoryFilter } from './Category'
import { toast } from "react-toastify";
const Food = () => {
    const { addMeal } = useCartStore()

    //    const data = getMenu()
    const { status: meal_status, data: meal_data } = useQuery({ queryKey: ["meals"], queryFn: getMenu, refetchOnMount: false });

    //   console.log(data);
    const [foods, setFoods] = useState(meal_data);

    useEffect(() => {
        if (meal_status === 'success') {
            setFoods(meal_data)
        }


    }, [meal_status])

    //   Filter Type burgers/pizza/etc
    const filterType = (category: number) => {
        setFoods(
            meal_data?.filter((item) => {
                return item.category === category;
            })
        );
    };
    const onAddMeal = (meal: any) => {
        addMeal(meal)
        toast("New Item Added")
    }
    return (
        <div className='max-w-[1640px] m-auto px-4 py-12'>

            <h1 className='text-orange-600 font-bold text-4xl text-center'>
                Top Rated Menu Items
            </h1>
            {/* Filter Row */}
            <div className='flex flex-col lg:flex-row justify-between'>
                {/* Fliter Type */}
                <div>
                    <div className='flex justfiy-between flex-wrap'>
                        <button
                            onClick={() => setFoods(meal_data)}
                            className='m-1 border-orange-600 text-orange-600 hover:bg-orange-600 hover:text-white'
                        >
                            All
                        </button>
                        <CategoryFilter onClickHandler={filterType} />
                    </div>
                </div>

            </div>

            <div className='grid grid-cols-2 lg:grid-cols-4 gap-6 pt-4'>
                {foods?.map((item, index) => (
                    <div key={index} className="relative group cursor-pointer border shadow-lg rounded-lg hover:scale-105 ">
                        <img src={item.image_url} alt={item.item_name} className="w-full h-[200px] object-cover rounded-t-lg" />
                        <div className="absolute inset-0 opacity-0 m-0 group-hover:opacity-60 flex items-center justify-center">
                            <button className="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg"
                                onClick={() => onAddMeal(item)}
                            >
                                <FaPlus className="text-4xl text-black p-2 z-10" />
                            </button>
                        </div>

                        <div className="flex justify-between px-2 py-4">
                            <p className="font-bold">{item.item_name}</p>
                            <p><span className="bg-orange-500 text-white p-1 rounded-md">{(item.price / 100).toLocaleString("en-US", { style: "currency", currency: "CAD" })}</span></p>
                        </div>
                    </div>

                ))}
            </div>
        </div >
    );
};

export default Food;
