export const useRouter = () => {
    return {
        push: (url: string) => {
            window.location.href = url;
        },
        replace: (url: string) => {
            window.location.replace(url);
        },
        back: () => {
            window.history.back();
        },
        pathname: window.location.pathname,
        query: {},
        asPath: window.location.pathname + window.location.search
    };
};
