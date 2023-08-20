import Image from 'next/image'
import styles from './page.module.css'
import Link from 'next/link'
import './styles.css'

export default function Home() {
  return (
    <main>
      <div className="centered">Bienvenue sur Paradoxi Front ! Ton jukebox pour tes musiques préférées !
        <Link href="/login">Connecte toi !</Link>
        <Link href="/register">Créer ton compte !</Link>
      </div>
    </main>
  )
}
