export default function Input({placeholder, type ="text"}){
    return(
        <input
            type={type}
            placeholder={placeholder}
            className=" w-full px-3 py-2 text-sm border rounded-md outline-none focus:ring-blue-500"
        />
    );
}