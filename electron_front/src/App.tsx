import { useState } from 'react';
import Playlist from './models/Playlist';
import PlaylistComponent from './components/Playlist';
import Video from './models/Video';

function App() {
  const [path, setPath] = useState('');
  const [playlists] = useState([
    new Playlist("ACUnity", "/home/sample/videos/ACUnity", [new Video("ep1", "/home/sample/videos/teste/ep1.mp4")]),
    new Playlist("RDR2", "/home/sample/videos/RDR2", [
      new Video("ep1", "/home/sample/videos/RDR2/ep1.mp4"),
      new Video("ep2", "/home/sample/videos/RDR2/ep2.mp4"),
    ]),
    new Playlist("RDR2", "/home/sample/videos/RDR2", [
      new Video("ep1", "/home/sample/videos/RDR2/ep1.mp4"),
      new Video("ep2", "/home/sample/videos/RDR2/ep2.mp4"),
    ]),
    new Playlist("RDR2", "/home/sample/videos/RDR2", [
      new Video("ep1", "/home/sample/videos/RDR2/ep1.mp4"),
      new Video("ep2", "/home/sample/videos/RDR2/ep2.mp4"),
    ]),
    new Playlist("RDR2", "/home/sample/videos/RDR2", [
      new Video("ep1", "/home/sample/videos/RDR2/ep1.mp4"),
      new Video("ep2", "/home/sample/videos/RDR2/ep2.mp4"),
    ]),
    new Playlist("RDR2", "/home/sample/videos/RDR2", [
      new Video("ep1", "/home/sample/videos/RDR2/ep1.mp4"),
      new Video("ep2", "/home/sample/videos/RDR2/ep2.mp4"),
    ]),
  ])

  const handleDirectoryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPath(event.target.value);
  };

  return (
    <main className='flex flex-col items-center justify-center min-h-screen'>
      <div className='p-2'>
        <h1 className='text-4xl'>Uploader</h1>
        <div className='flex py-1'>
          <p className='text-xl w-5/12'>Choose your videos path:</p>
          <input className='border-2 rounded outline-none p-1 focus:border-blue-400 w-7/12' type="text" onChange={handleDirectoryChange} />
        </div>
        {path && <p>Selected Directory: {path}</p>}
        {path &&
          <div className='flex-col w-full border-2 rounded py-1 px-2'>
            <h2 className='text-2xl'>Playlists:</h2>
            {playlists.map(playlist => {
              return (
                <PlaylistComponent playlist={playlist} />
              )
            })
            }
          </div>
        }
        {!path && <p>Path not selected</p>}
      </div>
    </main>
  );
}

export default App;